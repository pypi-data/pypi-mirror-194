import itertools
import re

import numpy as np
import pandas as pd
import pysam

from hits import sam, interval, utilities, fastq, sw
from .target_info import DegenerateDeletion, DegenerateInsertion

from .outcome_record import Integration

import knock_knock.outcome

memoized_property = utilities.memoized_property
memoized_with_args = utilities.memoized_with_args
idx = pd.IndexSlice

class Categorizer:
    def __init__(self, alignments, target_info, **kwargs):
        self.alignments = alignments
        self.target_info = target_info

        alignment = alignments[0]
        self.name = alignment.query_name
        self.query_name = self.name
        self.seq = sam.get_original_seq(alignment)
        self.qual = sam.get_original_qual(alignment)

        self.read = sam.mapping_to_Read(alignment)

    @memoized_property
    def whole_read(self):
        return interval.Interval(0, len(self.seq) - 1)

    @classmethod
    def full_index(cls):
        full_index = []
        for cat, subcats in cls.category_order:
            for subcat in subcats:
                full_index.append((cat, subcat))
                
        full_index = pd.MultiIndex.from_tuples(full_index) 

        return full_index
    
    @classmethod
    def categories(cls):
        return [c for c, scs in cls.category_order]
    
    @classmethod
    def subcategories(cls):
        return dict(cls.category_order)

    @classmethod
    def order(cls, outcome):
        if isinstance(outcome, tuple):
            category, subcategory = outcome

            try:
                return (cls.categories().index(category),
                        cls.subcategories()[category].index(subcategory),
                       )
            except:
                raise ValueError(category, subcategory)
        else:
            category = outcome
            try:
                return cls.categories().index(category)
            except:
                raise ValueError(category)

    @classmethod
    def outcome_to_sanitized_string(cls, outcome):
        if isinstance(outcome, tuple):
            c, s = cls.order(outcome)
            return f'category{c:03d}_subcategory{s:03d}'
        else:
            c = cls.order(outcome)
            return f'category{c:03d}'

    @classmethod
    def sanitized_string_to_outcome(cls, sanitized_string):
        match = re.match('category(\d+)_subcategory(\d+)', sanitized_string)
        if match:
            c, s = map(int, match.groups())
            category, subcats = cls.category_order[c]
            subcategory = subcats[s]
            return category, subcategory
        else:
            match = re.match('category(\d+)', sanitized_string)
            if not match:
                raise ValueError(sanitized_string)
            c = int(match.group(1))
            category, subcats = cls.category_order[c]
            return category

    def q_to_feature_offset(self, al, feature_name, target_info=None):
        ''' Returns dictionary of 
                {true query position: offset into feature relative to its strandedness
                 (i.e. from the start of + stranded and from the right of - stranded)
                }
        '''
        if al is None:
            return {}

        if target_info is None:
            target_info = self.target_info

        if (al.reference_name, feature_name) not in target_info.features:
            return {}

        ref_p_to_feature_offset = target_info.ref_p_to_feature_offset(al.reference_name, feature_name)
        seq = target_info.reference_sequences[al.reference_name]
        
        q_to_feature_offset = {}
        
        for q, read_b, ref_p, ref_b, qual in sam.aligned_tuples(al, seq):
            if q is not None and ref_p in ref_p_to_feature_offset:
                q_to_feature_offset[q] = ref_p_to_feature_offset[ref_p]
                
        return q_to_feature_offset

    def feature_offset_to_q(self, al, feature_name, target_info=None):
        return utilities.reverse_dictionary(self.q_to_feature_offset(al, feature_name, target_info=target_info))

    def feature_interval(self, al, feature_name, target_info=None):
        ''' Returns the query interval aligned to feature_name by al. '''
        qs = self.q_to_feature_offset(al, feature_name, target_info=target_info)
        if len(qs) == 0:
            return interval.Interval.empty()
        else:
            return interval.Interval(min(qs), max(qs))

    def share_feature(self, first_al, first_feature_name, second_al, second_feature_name):
        '''
        Returns True if any query position is aligned to equivalent positions in first_feature and second_feature
        by first_al and second_al.
        '''
        if first_al is None or second_al is None:
            return False
        
        first_q_to_offsets = self.q_to_feature_offset(first_al, first_feature_name)
        second_q_to_offsets = self.q_to_feature_offset(second_al, second_feature_name)
        
        share_any = any(second_q_to_offsets.get(q) == offset for q, offset in first_q_to_offsets.items())

        return share_any

    def are_mutually_extending_from_shared_feature(self,
                                                   left_al, left_feature_name,
                                                   right_al, right_feature_name,
                                                  ):
        ti = self.target_info
        
        results = None

        if self.share_feature(left_al, left_feature_name, right_al, right_feature_name):
            switch_results = sam.find_best_query_switch_after(left_al,
                                                              right_al,
                                                              ti.reference_sequences[left_al.reference_name],
                                                              ti.reference_sequences[right_al.reference_name],
                                                              min,
                                                             )
                                                        
            # Does an optimal switch point occur somewhere in the shared feature?

            switch_interval = interval.Interval(min(switch_results['best_switch_points']), max(switch_results['best_switch_points']))
            
            left_qs = self.q_to_feature_offset(left_al, left_feature_name)
            left_feature_interval = interval.Interval(min(left_qs), max(left_qs))                    

            right_qs = self.q_to_feature_offset(right_al, right_feature_name)
            right_feature_interval = interval.Interval(min(right_qs), max(right_qs))                    

            # Heuristic: if an optimal switch point occurs in the shared feature,
            # any amount of sequence past the shared feature is enough.
            # If the optimal switch point is outside, require a longer amount. 
            # Motivation: for replacement edits in which pegRNA sequence is similar
            # to genomic sequence, we want to avoid identifying false positive
            # extension alignments that are actually just genomic sequence, while
            # still allowing the possibility of partial replacements that retain 
            # some genomic sequence after the transition.

            switch_in_shared = switch_interval & left_feature_interval

            left_reaches_ref_end = left_al.reference_end == len(ti.reference_sequences[left_al.reference_name])
            right_reaches_ref_end = right_al.reference_end == len(ti.reference_sequences[right_al.reference_name])
            both_reach_ref_end = left_reaches_ref_end and right_reaches_ref_end

            # If as much query as possible is attributed to the right al, does the remaining left al
            # still explain part of the read to the left of the overlapping feature?

            cropped_left_al = sam.crop_al_to_query_int(left_al, 0, switch_interval.start)
            left_of_feature = interval.Interval(0, left_feature_interval.start - 1)
            left_contribution_past_overlap = interval.get_covered(cropped_left_al) & left_of_feature

            if (switch_in_shared and left_contribution_past_overlap.total_length > 0) or (left_contribution_past_overlap.total_length >= 10) or both_reach_ref_end:
                cropped_left_al = sam.crop_al_to_query_int(left_al, 0, switch_interval.end)
            
                # Similarly, if as much query as possible is attributed to the left al, does the remaining right al
                # still explain part of the read to the right of the overlapping feature?

                cropped_right_al = sam.crop_al_to_query_int(right_al, switch_interval.end + 1, self.whole_read.end)
                right_of_feature = interval.Interval(right_feature_interval.end + 1, self.whole_read.end)
                right_contributes_past_overlap = interval.get_covered(cropped_right_al) & right_of_feature

                overlap_reaches_read_end = right_of_feature.is_empty

                if right_contributes_past_overlap or overlap_reaches_read_end or both_reach_ref_end:
                    cropped_right_al = sam.crop_al_to_query_int(right_al, switch_interval.start + 1, len(self.seq))

                    if right_contributes_past_overlap:
                        status = 'definite'
                    else:
                        status = 'reaches end'

                    results = {
                        'status': status,
                        'alignments': {
                            'left': left_al,
                            'right': right_al,
                        },
                        'cropped_alignments': {
                            'left': cropped_left_al,
                            'right': cropped_right_al,
                        },
                    }

        return results

    def extend_alignment_from_shared_feature(self,
                                             alignment_to_extend,
                                             feature_name_in_alignment,
                                             ref_to_search,
                                             feature_name_in_ref,
                                            ):
        ''' Generates the longest perfectly extended alignment to ref_to_search
        that pairs feature_name_in_alignment in alignment_to_extend with feature_name_in_ref.
        Motivation: if a potential transition occurs close to the end of a read or otherwise
        only involves a small amount of sequence past the transition, initial alignment
        generation may fail to identify a potentially relevant alignment.
        ''' 

        ti = self.target_info

        feature_in_alignment = ti.features[alignment_to_extend.reference_name, feature_name_in_alignment]
        feature_al = sam.crop_al_to_feature(alignment_to_extend, feature_in_alignment)

        # Only extend if the alignment cleanly covers the whole feature.
        covers_whole_feature = sam.feature_overlap_length(feature_al, feature_in_alignment) == len(feature_in_alignment)

        if covers_whole_feature and not sam.contains_indel(feature_al):
            # Create a new alignment covering the feature on ref_to_search,
            # which will then be used as input to sw.extend_alignment.
            # This needs three things:
            #   - the query interval to be covered, which will be converted
            #     into lengths to soft clip before and after the alignment.
            #   - the reference interval to be covered, which will have its
            #     left-most value put into reference_start.
            #   - whether or not the alignment is reversed, which will be
            #     reflected in the relevant flag and by flipped seq, qual,
            #     and cigar.

            # Get the query interval covered.
            al_q_to_feature_offset = self.q_to_feature_offset(alignment_to_extend, feature_name_in_alignment)
            query_interval = interval.Interval(min(al_q_to_feature_offset), max(al_q_to_feature_offset))

            # Get the ref interval covered.
            feature_in_ref = ti.features[ref_to_search, feature_name_in_ref]
            ref_interval = interval.Interval(feature_in_ref.start, feature_in_ref.end)

            # Figure out the strand.
            if feature_in_ref.strand == feature_in_alignment.strand:
                is_reverse = alignment_to_extend.is_reverse
            else:
                is_reverse = not alignment_to_extend.is_reverse

            al = pysam.AlignedSegment(ti.header)

            al.query_sequence = self.seq
            al.query_qualities = self.qual

            soft_clip_before = query_interval.start
            soft_clip_after = len(self.seq) - 1 - query_interval.end

            al.cigar = [
                (sam.BAM_CSOFT_CLIP, soft_clip_before),
                (sam.BAM_CMATCH, feature_al.query_alignment_length),
                (sam.BAM_CSOFT_CLIP, soft_clip_after),
            ]

            if is_reverse:
                # Need to extract query_qualities before overwriting query_sequence.
                flipped_query_qualities = al.query_qualities[::-1]
                al.query_sequence = utilities.reverse_complement(al.query_sequence)
                al.query_qualities = flipped_query_qualities
                al.is_reverse = True
                al.cigar = al.cigar[::-1]

            al.reference_name = ref_to_search
            al.query_name = self.read.name
            al.next_reference_id = -1

            al.reference_start = ref_interval.start

            extended_al = sw.extend_alignment(al, ti.reference_sequence_bytes[ref_to_search])
        else:
            extended_al = None

        return extended_al

class Layout(Categorizer):
    category_order = [
        ('WT',
            ('WT',
            ),
        ),
        ('simple indel',
            ('insertion',
             'deletion',
             'deletion <50 nt',
             'deletion >=50 nt',
            ),
        ),
        ('complex indel',
            ('complex indel',
             'multiple indels',
            ),
        ),
        ('HDR',
            ('HDR',
            ),
        ),
        ('blunt misintegration',
            ("5' HDR, 3' blunt",
             "5' blunt, 3' HDR",
             "5' blunt, 3' blunt",
             "5' blunt, 3' imperfect",
             "5' imperfect, 3' blunt",
            ),
        ),
        ('incomplete HDR',
            ("5' HDR, 3' imperfect",
             "5' imperfect, 3' HDR",
            ),
        ),
        ('donor fragment',
            ("5' imperfect, 3' imperfect",
            ),
        ),
        ('complex misintegration',
            ('complex misintegration',
            ),
        ),
        ('concatenated misintegration',
            ('HDR',
             '5\' blunt',
             '3\' blunt',
             '5\' and 3\' blunt',
             'incomplete',
            ),
        ),
        ('non-homologous donor',
            ('simple',
             'complex',
            ),
        ),
        ('genomic insertion',
            ('hg38',
             'hg19',
             'mm10',
             'e_coli',
            ),
        ),
        ('uncategorized',
            ('uncategorized',
             'donor with indel',
             'mismatch(es) near cut',
             'multiple indels near cut',
             'donor specific present',
             'other',
            ),
        ),
        ('unexpected source',
            ('flipped',
             'e coli',
             'uncategorized',
            ),
        ),
        ('nonspecific amplification',
            ('hg38',
             'hg19',
             'mm10',
            ),
        ),
        ('malformed layout',
            ('extra copy of primer',
             'missing a primer',
             'too short',
             'primer far from read edge',
             'primers not in same orientation',
             'no alignments detected',
            ),
        ),
        ('bad sequence',
            ('non-overlapping',
            ),
        ),
    ]

    def __init__(self, alignments, target_info, error_corrected=False, mode='illumina'):
        self.mode = mode

        if mode == 'illumina':
            self.max_indel_allowed_in_donor = 1
        elif mode == 'pacbio':
            self.max_indel_allowed_in_donor = 3

        self.target_info = target_info

        self.error_corrected = error_corrected

        self.original_alignments = [al for al in alignments if not al.is_unmapped]
        self.unmapped_alignments = [al for al in alignments if al.is_unmapped]

        alignment = alignments[0]
        self.name = alignment.query_name
        self.query_name = self.name
        self.seq = sam.get_original_seq(alignment)
        self.qual = np.array(sam.get_original_qual(alignment))

        self.relevant_alignments = self.original_alignments

        self.ignore_target_outside_amplicon = True

        if self.seq is None:
            length = 0
        else:
            length = len(self.seq)

        self.inferred_amplicon_length = length
        self.categorized = False

    @memoized_property
    def target_alignments(self):
        if self.seq is None:
            return []

        ti = self.target_info

        primers = ti.primers_by_side_of_target
        target_seq_bytes = ti.reference_sequence_bytes[ti.target]

        original_als = [al for al in self.original_alignments if al.reference_name == ti.target]

        processed_als = []

        for al in original_als:
            if self.ignore_target_outside_amplicon:
                # Ignore alignments to the target that fall entirely outside the amplicon interval.
                # These should typically be considered genomic insertions and caught by supplementary alignments;
                # counting on target alignments to get them would make behavior dependent on the amount of flanking
                # sequence included around the amplicon.
                if not (ti.amplicon_interval & sam.reference_interval(al)):
                    continue

            query_interval = interval.get_covered(al)

            # Primers frequently contain 1 nt deletions, sometimes causing truncated alignments at the edges
            # of reads. If alignment ends close to but not at a read end, try to refine.
            extend_before = (0 < query_interval.start <= len(primers[5]) + 5)
            extend_after = (len(self.seq) - 1 - len(primers[3]) - 5 <= query_interval.end < len(self.seq) - 1)
            if extend_before or extend_after:
                al = sw.extend_repeatedly(al, target_seq_bytes, extend_before=extend_before, extend_after=extend_after)

            split_als = comprehensively_split_alignment(al, ti, self.mode)

            extended = [sw.extend_alignment(split_al, target_seq_bytes) for split_al in split_als]

            processed_als.extend(extended)

        # If processed alignments don't cover either edge, this typically means non-specific amplification.
        # Try to realign each uncovered edge to the relevant primer to check for this.
        existing_covered = interval.get_disjoint_covered(processed_als)

        possible_edge_als = []

        if existing_covered.start != 0:
            possible_edge_als.append(self.realign_edges_to_primers(5))

        if existing_covered.end != len(self.seq) - 1:
            possible_edge_als.append(self.realign_edges_to_primers(3))

        for edge_al in possible_edge_als:
            if edge_al is not None:
                new_covered = interval.get_covered(edge_al) - existing_covered
                # Only add the new alignment if it explains a substantial new amount of the read.
                if new_covered.total_length > 10:
                    processed_als.append(edge_al)
        
        return processed_als

    @memoized_property
    def donor_alignments(self):
        if self.target_info.donor is None:
            return []

        original_als = [al for al in self.original_alignments if al.reference_name == self.target_info.donor]
        processed_als = []

        for al in original_als:
            split_als = comprehensively_split_alignment(al, self.target_info, self.mode)
            processed_als.extend(split_als)

        return processed_als
    
    @memoized_property
    def nonhomologous_donor_alignments(self):
        if self.target_info.nonhomologous_donor is None:
            return []

        original_als = [al for al in self.original_alignments if al.reference_name == self.target_info.nonhomologous_donor]
        processed_als = []

        for al in original_als:
            split_als = comprehensively_split_alignment(al, self.target_info, self.mode)
            processed_als.extend(split_als)

        return processed_als

    @memoized_property
    def nonredundant_supplemental_alignments(self):
        primary_als = self.parsimonious_and_gap_alignments + self.nonhomologous_donor_alignments + self.extra_alignments
        covered = interval.get_disjoint_covered(primary_als)

        supp_als_to_keep = []

        for al in self.supplemental_alignments:
            if interval.get_covered(al) - covered:
                supp_als_to_keep.append(al)

        supp_als_to_keep = sorted(supp_als_to_keep, key=lambda al: al.query_alignment_length, reverse=True)
        return supp_als_to_keep

    @memoized_property
    def alignments(self):
        return self.target_alignments + self.donor_alignments
    
    @memoized_property
    def supplemental_alignments(self):
        als = [al for al in self.original_alignments if al.reference_name not in self.target_info.reference_sequences]

        # For performance reasons, cap the number of alignments considered, prioritizing
        # alignments that explain more matched bases.
        def priority(al):
            return al.query_alignment_length - al.get_tag('NM')

        best_als = sorted(als, key=priority, reverse=True)[:100]

        split_als = []
        for al in best_als:
            split_als.extend(sam.split_at_large_insertions(al, 10))

        return split_als

    @memoized_property
    def extra_alignments(self):
        ti = self.target_info
        extra_ref_names = {n for n in ti.reference_sequences if n not in [ti.target, ti.donor]}
        als = [al for al in self.original_alignments if al.reference_name in extra_ref_names]
        return als

    @memoized_with_args
    def whole_read_minus_edges(self, edge_length):
        return interval.Interval(edge_length, len(self.seq) - 1 - edge_length)

    def register_deletion(self):
        self.category = 'simple indel'

        indel = self.indel_near_cut[0]

        if indel.kind == 'D':
            if indel.length < 50:
                self.subcategory = 'deletion <50 nt'
            else:
                self.subcategory = 'deletion >=50 nt'

        self.details = self.indel_string
        self.relevant_alignments = self.parsimonious_target_alignments

    def register_integration_details(self):
        ti = self.target_info
        donor_al = self.donor_specific_integration_alignments[0]

        if self.strand == '+':
            left_target_al = self.primer_alignments[5]
            right_target_al = self.primer_alignments[3]

            left_junction = sam.find_best_query_switch_after(left_target_al, donor_al, ti.target_sequence, ti.donor_sequence, min)
            right_junction = sam.find_best_query_switch_after(donor_al, right_target_al, ti.donor_sequence, ti.target_sequence, max)

            left_target_al_cropped = sam.crop_al_to_query_int(left_target_al, 0, left_junction['switch_after'])
            if left_target_al_cropped is not None:
                target_edge_before = left_target_al_cropped.reference_end - 1
            else:
                # This is an error condition.
                target_edge_before = -1

            right_target_al_cropped = sam.crop_al_to_query_int(right_target_al, right_junction['switch_after'] + 1, np.inf)
            if right_target_al_cropped is not None:
                target_edge_after = right_target_al_cropped.reference_start
            else:
                target_edge_after = -1

            donor_strand = sam.get_strand(donor_al)
        else:
            right_target_al = self.primer_alignments[5]
            left_target_al = self.primer_alignments[3]

            left_junction = sam.find_best_query_switch_after(left_target_al, donor_al, ti.target_sequence, ti.donor_sequence, min)
            right_junction = sam.find_best_query_switch_after(donor_al, right_target_al, ti.donor_sequence, ti.target_sequence, max)

            left_target_al_cropped = sam.crop_al_to_query_int(left_target_al, 0, left_junction['switch_after'])
            if left_target_al_cropped is not None:
                target_edge_after = left_target_al_cropped.reference_start
            else:
                target_edge_after = -1

            right_target_al_cropped = sam.crop_al_to_query_int(right_target_al, right_junction['switch_after'] + 1, np.inf)
            if right_target_al_cropped is not None:
                target_edge_before = right_target_al_cropped.reference_end - 1
            else:
                target_edge_before = -1

            # Unclear what the right approach to recording strand is here.
            donor_strand = sam.get_opposite_strand(donor_al)

        donor_al_cropped = sam.crop_al_to_query_int(donor_al, left_junction['switch_after'] + 1, right_junction['switch_after'])

        donor_start = donor_al_cropped.reference_start
        donor_end = donor_al_cropped.reference_end - 1

        mh_lengths = self.donor_microhomology

        integration = Integration(target_edge_before, target_edge_after, donor_strand, donor_start, donor_end, mh_lengths[5], mh_lengths[3])

        return str(integration)

    def register_nonspecific_amplification(self):
        als = self.nonspecific_amplification

        al = als[0]

        organism, original_al = self.target_info.remove_organism_from_alignment(al)

        self.category = 'nonspecific amplification'
        self.subcategory = organism
        self.details = 'n/a'

        self.relevant_alignments = interval.make_parsimonious(self.parsimonious_target_alignments + self.nonspecific_amplification)
    
    def categorize(self):
        if self.target_info.donor is None and self.target_info.nonhomologous_donor is None:
           c, s, d = self.categorize_no_donor()
        else:
            c, s, d = self.categorize_with_donor()
        
        if self.strand == '-':
            self.relevant_alignments = [sam.flip_alignment(al) for al in self.relevant_alignments]

        return c, s, d

    def categorize_with_donor(self):
        self.details = 'n/a'
        self.outcome = knock_knock.outcome.Outcome('')
        
        if self.seq is None or len(self.seq) <= self.target_info.combined_primer_length + 10:
            self.category = 'malformed layout'
            self.subcategory = 'too short'
            self.relevant_alignments = self.uncategorized_relevant_alignments

        elif all(al.is_unmapped for al in self.alignments):
            self.category = 'malformed layout'
            self.subcategory = 'no alignments detected'
            self.relevant_alignments = self.uncategorized_relevant_alignments

        elif self.extra_copy_of_primer:
            self.category = 'malformed layout'
            self.subcategory = 'extra copy of primer'
            self.relevant_alignments = self.uncategorized_relevant_alignments

        elif self.missing_a_primer:
            self.category = 'malformed layout'
            self.subcategory = 'missing a primer'
            self.relevant_alignments = self.uncategorized_relevant_alignments

        elif self.primer_strands[5] != self.primer_strands[3]:
            self.category = 'malformed layout'
            self.subcategory = 'primers not in same orientation'
            self.relevant_alignments = self.uncategorized_relevant_alignments
        
        elif not self.primer_alignments_reach_edges:
            self.category = 'malformed layout'
            self.subcategory = 'primer far from read edge'
            self.relevant_alignments = self.uncategorized_relevant_alignments

        elif not self.has_integration:
            if self.indel_near_cut is not None:
                self.details = self.indel_string
                self.relevant_alignments = self.parsimonious_target_alignments

                if len(self.indel_near_cut) > 1:
                    self.category = 'uncategorized'
                    self.subcategory = 'multiple indels near cut'
                else:
                    self.category = 'simple indel'

                    indel = self.indel_near_cut[0]

                    if indel.kind == 'D':
                        if indel.length < 50:
                            self.subcategory = 'deletion <50 nt'
                        else:
                            self.subcategory = 'deletion >=50 nt'

                        self.outcome = knock_knock.outcome.DeletionOutcome.from_string(self.details)

                    elif indel.kind == 'I':
                        self.subcategory = 'insertion'
                        self.outcome = knock_knock.outcome.InsertionOutcome.from_string(self.details)

            elif len(self.mismatches_near_cut) > 0:
                self.category = 'uncategorized'
                self.subcategory = 'mismatch(es) near cut'
                self.details = 'n/a'
                self.relevant_alignments = self.uncategorized_relevant_alignments

            else:
                self.category = 'WT'
                self.subcategory = 'WT'
                self.relevant_alignments = self.parsimonious_target_alignments

        elif self.integration_summary == 'donor':
            junctions = set(self.junction_summary_per_side.values())

            if junctions == set(['HDR']):
                self.category = 'HDR'
                self.subcategory = 'HDR'
                self.relevant_alignments = self.parsimonious_and_gap_alignments

            elif self.gap_covered_by_target_alignment:
                self.category = 'complex indel'
                self.subcategory = 'complex indel'
                self.details = 'n/a'
                self.relevant_alignments = self.parsimonious_and_gap_alignments

            elif junctions == set(['imperfect']):
                if self.not_covered_by_simple_integration.total_length >= 2:
                    self.category = 'complex misintegration'
                    self.subcategory = 'complex misintegration'
                else:
                    self.category = 'donor fragment'
                    self.subcategory = f'5\' {self.junction_summary_per_side[5]}, 3\' {self.junction_summary_per_side[3]}'
                    self.details = self.register_integration_details()

                self.relevant_alignments = self.parsimonious_and_gap_alignments

            else:
                self.subcategory = f'5\' {self.junction_summary_per_side[5]}, 3\' {self.junction_summary_per_side[3]}'

                if 'blunt' in junctions:
                    self.category = 'blunt misintegration'
                    self.details = self.register_integration_details()

                elif junctions == set(['imperfect', 'HDR']):
                    if self.not_covered_by_refined_alignments.total_length >= 2:
                        self.category = 'complex misintegration'
                        self.subcategory = 'complex misintegration'
                    else:
                        self.category = 'incomplete HDR'

                    self.details = self.register_integration_details()
                else:
                    self.category = 'complex misintegration'
                    self.subcategory = 'complex misintegration'
                    self.details = 'n/a'

                self.relevant_alignments = self.parsimonious_and_gap_alignments
        
        # TODO: check here for HA extensions into donor specific
        elif self.gap_covered_by_target_alignment:
            self.category = 'complex indel'
            self.subcategory = 'complex indel'
            self.details = 'n/a'
            self.relevant_alignments = self.parsimonious_and_gap_alignments

        elif self.integration_interval.total_length <= 5:
            if self.target_to_at_least_cut[5] and self.target_to_at_least_cut[3]:
                self.category = 'simple indel'
                self.subcategory = 'insertion'
            else:
                self.category = 'complex indel'
                self.subcategory = 'complex indel'
            self.details = 'n/a'
            self.relevant_alignments = self.parsimonious_and_gap_alignments

        elif self.integration_summary == 'concatamer':
            if self.target_info.donor_type == 'plasmid':
                self.category = 'complex misintegration'
                self.subcategory = 'complex misintegration'
                self.details = 'n/a'
            else:
                self.category = 'concatenated misintegration'
                self.subcategory = self.junction_summary
                self.details = self.register_integration_details()

            self.relevant_alignments = self.parsimonious_and_gap_alignments

        elif self.nonhomologous_donor_integration is not None:
            self.category = 'non-homologous donor'
            self.subcategory = 'simple'

            NH_al = self.nonhomologous_donor_alignments[0]
            NH_strand = sam.get_strand(NH_al)
            MH_nts = self.NH_donor_microhomology
            self.details = f'{NH_strand},{MH_nts[5]},{MH_nts[3]}'
            
            self.relevant_alignments = self.parsimonious_target_alignments + self.nonhomologous_donor_alignments

        elif self.nonspecific_amplification is not None:
            self.register_nonspecific_amplification()

        elif self.genomic_insertion is not None:
            self.register_genomic_insertion()

        elif self.partial_nonhomologous_donor_integration is not None:
            self.category = 'non-homologous donor'
            self.subcategory = 'complex'
            self.details = 'n/a'
            
            self.relevant_alignments = self.parsimonious_target_alignments + self.nonhomologous_donor_alignments + self.nonredundant_supplemental_alignments
        
        elif self.any_donor_specific_present:
            self.category = 'complex misintegration'
            self.subcategory = 'complex misintegration'
            self.details = 'n/a'
            self.relevant_alignments = self.uncategorized_relevant_alignments

        elif self.integration_summary in ['donor with indel', 'other', 'unexpected length', 'unexpected source']:
            self.category = 'uncategorized'
            self.subcategory = self.integration_summary

            self.relevant_alignments = self.uncategorized_relevant_alignments

        else:
            print(self.integration_summary)

        return self.category, self.subcategory, self.details
    
    def categorize_no_donor(self):
        self.details = 'n/a'

        if self.seq is None or len(self.seq) <= self.target_info.combined_primer_length + 15:
            self.category = 'malformed layout'
            self.subcategory = 'too short'
            self.relevant_alignments = self.uncategorized_relevant_alignments

        elif all(al.is_unmapped for al in self.alignments):
            self.category = 'malformed layout'
            self.subcategory = 'no alignments detected'
            self.relevant_alignments = self.uncategorized_relevant_alignments

        elif self.extra_copy_of_primer:
            self.category = 'malformed layout'
            self.subcategory = 'extra copy of primer'
            self.relevant_alignments = self.uncategorized_relevant_alignments

        elif self.missing_a_primer:
            self.category = 'malformed layout'
            self.subcategory = 'missing a primer'
            self.relevant_alignments = self.uncategorized_relevant_alignments

        elif self.primer_strands[5] != self.primer_strands[3]:
            self.category = 'malformed layout'
            self.subcategory = 'primers not in same orientation'
            self.relevant_alignments = self.uncategorized_relevant_alignments
        
        elif not self.primer_alignments_reach_edges:
            self.category = 'malformed layout'
            self.subcategory = 'primer far from read edge'
            self.relevant_alignments = self.uncategorized_relevant_alignments

        elif self.single_merged_primer_alignment is not None:
            num_indels = len(self.all_indels_near_cuts)
            if num_indels > 0:
                if num_indels > 1:
                    self.category = 'complex indel'
                    self.subcategory = 'multiple indels'
                else:
                    self.category = 'simple indel'
                    indel = self.indel_near_cut[0]
                    if indel.kind == 'D':
                        if indel.length < 50:
                            self.subcategory = 'deletion <50 nt'
                        else:
                            self.subcategory = 'deletion >=50 nt'
                    elif indel.kind == 'I':
                        self.subcategory = 'insertion'

                # Split at every indel
                if self.mode == 'illumina':
                    split_at_both = []

                    for al in self.parsimonious_target_alignments:
                        split_at_dels = sam.split_at_deletions(al, 1)
                        for split_al in split_at_dels:
                            split_at_both.extend(sam.split_at_large_insertions(split_al, 1))
                    self.relevant_alignments = split_at_both
                else:
                    self.relevant_alignments = self.parsimonious_target_alignments

                self.details = ' '.join(map(str, self.all_indels_near_cuts))
            else:
                self.category = 'WT'
                self.subcategory = 'WT'
                self.relevant_alignments = self.parsimonious_target_alignments
        
        elif self.nonspecific_amplification is not None:
            self.register_nonspecific_amplification()

        elif self.genomic_insertion is not None:
            self.register_genomic_insertion()

        else:
            self.category = 'uncategorized'
            self.subcategory = 'uncategorized'
            self.details = 'n/a'

        return self.category, self.subcategory, self.details
    
    @memoized_property
    def read(self):
        if self.seq is None:
            return None
        else:
            return fastq.Read(self.name, self.seq, fastq.encode_sanger(self.qual))
    
    def realign_edges_to_primers(self, read_side):
        if self.seq is None:
            return []

        buffer_length = 5

        target_seq = self.target_info.target_sequence

        edge_als = []

        for amplicon_side in [5, 3]:
            primer = self.target_info.primers_by_side_of_target[amplicon_side]

            if amplicon_side == 5:
                amplicon_slice = idx[primer.start:primer.end + 1 + buffer_length]
            else:
                amplicon_slice = idx[primer.start - buffer_length:primer.end + 1]

            amplicon_side_seq = target_seq[amplicon_slice]

            if read_side == 5:
                read_slice = idx[:len(primer) + buffer_length]
            else:
                read_slice = idx[-(len(primer) + buffer_length):]

            if amplicon_side == 5:
                alignment_type = 'fixed_start'
            else:
                alignment_type = 'fixed_end'

            read = self.read[read_slice]
            if amplicon_side != read_side:
                read = read.reverse_complement()

            soft_clip_length = len(self.seq) - len(read)

            targets = [('amplicon_side', amplicon_side_seq)]
            temp_header = pysam.AlignmentHeader.from_references([n for n, s in targets], [len(s) for n, s in targets])

            als = sw.align_read(read, targets, 5, temp_header,
                                alignment_type=alignment_type,
                                max_alignments_per_target=1,
                                both_directions=False,
                                min_score_ratio=0,
                               )

            # The fixed edge alignment strategy used can produce alignments that start or 
            # end with a deletion. Remove these.
            als = [sam.remove_terminal_deletions(al) for al in als]

            if len(als) > 0:
                al = als[0]

                if amplicon_side == 5:
                    ref_start_offset = primer.start
                    new_cigar = al.cigar + [(sam.BAM_CSOFT_CLIP, soft_clip_length)]
                else:
                    ref_start_offset = primer.start - buffer_length
                    new_cigar = [(sam.BAM_CSOFT_CLIP, soft_clip_length)] + al.cigar

                if read_side == 5:
                    primer_query_interval = interval.Interval(0, len(primer) - 1)
                elif read_side == 3:
                    # can't just use buffer_length as start in case read is shorter than primer + buffer_length
                    primer_query_interval = interval.Interval(len(read) - len(primer), np.inf)

                if amplicon_side != read_side:
                    al = sam.flip_alignment(al)

                edits_in_primer = sam.edit_distance_in_query_interval(al, primer_query_interval, ref_seq=amplicon_side_seq)

                if edits_in_primer <= 5:
                    al.reference_start = al.reference_start + ref_start_offset
                    al.cigar = sam.collapse_soft_clip_blocks(new_cigar)
                    if al.is_reverse:
                        seq = utilities.reverse_complement(self.seq)
                        qual = self.qual[::-1]
                    else:
                        seq = self.seq
                        qual = self.qual
                    al.query_sequence = seq
                    al.query_qualities = qual
                    al_dict = al.to_dict()
                    al_dict['ref_name'] = self.target_info.target
                    edge_al = pysam.AlignedSegment.from_dict(al_dict, self.target_info.header)
                    edge_als.append((edits_in_primer, edge_al))

        edge_als = sorted(edge_als, key=lambda t: t[0])
        if len(edge_als) == 0:
            edge_al = None
        else:
            edge_al = edge_als[0][1]
            
        return edge_al

    @memoized_property
    def all_primer_alignments(self):
        ''' Get all alignments that contain the amplicon primers. '''
        als = {}
        for side, primer in self.target_info.primers_by_side_of_target.items():
            # Prefer to have the primers annotated on the strand they anneal to,
            # so don't require strand match here.
            als[side] = [al for al in self.parsimonious_alignments if sam.overlaps_feature(al, primer, False)]

        return als

    @memoized_property
    def gap_alignments(self):
        gap_als = []

        gap = self.gap_between_primer_alignments
        if len(gap) >= 4:
            seq_bytes = self.seq.encode()
            for on in ['target', 'donor']:
                aligner = self.target_info.seed_and_extender[on]
                als = aligner(seq_bytes, gap.start, gap.end, self.name)
                als = sorted(als, key=lambda al: al.query_alignment_length, reverse=True)
                # For same reasoning as in target_alignments, only consider als that overlap the amplicon interval.
                if on == 'target':
                    als = [al for al in als if (self.target_info.amplicon_interval & sam.reference_interval(al))]

                gap_als.extend(als[:10])

        return gap_als

    @memoized_property
    def not_covered_by_initial_alignments(self):
        uncovered = self.whole_read - interval.get_disjoint_covered(self.alignments)
        return uncovered

    @memoized_property
    def not_covered_by_refined_alignments(self):
        uncovered = self.whole_read - interval.get_disjoint_covered(self.parsimonious_and_gap_alignments)
        return uncovered

    @memoized_property
    def not_covered_by_simple_integration(self):
        ''' Length of read not covered by primer edge alignments and the
        longest parsimonious donor integration alignment.
        '''

        donor_al = self.donor_specific_integration_alignments[0]
        als = [donor_al, self.primer_alignments[5], self.primer_alignments[3]]
        uncovered = self.whole_read - interval.get_disjoint_covered(als)
        return uncovered

    @memoized_property
    def sw_gap_alignments(self):
        ti = self.target_info

        gap_covers = []
        
        target_interval = ti.amplicon_interval
        
        for gap in self.not_covered_by_initial_alignments:
            if gap.total_length == 1:
                continue

            start = max(0, gap.start - 5)
            end = min(len(self.seq) - 1, gap.end + 5)
            extended_gap = interval.Interval(start, end)

            als = sw.align_read(self.read,
                                [(ti.target, ti.target_sequence),
                                ],
                                4,
                                ti.header,
                                N_matches=False,
                                max_alignments_per_target=5,
                                read_interval=extended_gap,
                                ref_intervals={ti.target: target_interval},
                                mismatch_penalty=-2,
                               )

            als = [sw.extend_alignment(al, ti.reference_sequence_bytes[ti.target]) for al in als]
            
            gap_covers.extend(als)

            if ti.donor is not None:
                als = sw.align_read(self.read,
                                    [(ti.donor, ti.donor_sequence),
                                    ],
                                    4,
                                    ti.header,
                                    N_matches=False,
                                    max_alignments_per_target=5,
                                    read_interval=extended_gap,
                                    mismatch_penalty=-2,
                                )

                als = [sw.extend_alignment(al, ti.reference_sequence_bytes[ti.donor]) for al in als]
                
                gap_covers.extend(als)

        return gap_covers

    @memoized_property
    def possibly_imperfect_gap_alignments(self):
        gap_als = []
        if self.gap_between_primer_alignments.total_length >= 10:
            for al in self.target_alignments:
                if (self.integration_interval - interval.get_covered(al)).total_length <= 2:
                    gap_als.append(al)

        return gap_als

    @memoized_property
    def all_target_gap_alignments(self):
        all_gap_als = self.gap_alignments + self.possibly_imperfect_gap_alignments
        return [al for al in all_gap_als if al.reference_name == self.target_info.target]

    @memoized_property
    def gap_covered_by_target_alignment(self):
        return len(self.all_target_gap_alignments) > 0

    @memoized_property
    def extra_copy_of_primer(self):
        ''' Check if too many alignments containing either primer were found. '''
        return any(len(als) > 1 for side, als in self.all_primer_alignments.items())
    
    @memoized_property
    def missing_a_primer(self):
        ''' Check if either primer was not found in an alignments. '''
        return any(len(als) == 0 for side, als in self.all_primer_alignments.items())
        
    @memoized_property
    def primer_alignments(self):
        ''' Get the single alignment containing each primer. '''
        primer_als = {5: None, 3: None}
        for side in [5, 3]:
            if len(self.all_primer_alignments[side]) == 1:
                primer_als[side] = self.all_primer_alignments[side][0]

        return primer_als
        
    @memoized_property
    def primer_strands(self):
        ''' Get which strand each primer-containing alignment mapped to. '''
        strands = {5: None, 3: None}
        for side in [5, 3]:
            al = self.primer_alignments[side]
            if al is not None:
                strands[side] = sam.get_strand(al)
        return strands
    
    @memoized_property
    def strand(self):
        ''' Get the single strand any primer-containing alignments mapped to. '''
        strands = set(self.primer_strands.values())

        if None in strands:
            strands.remove(None)

        if len(strands) != 1:
            return None
        else:
            return strands.pop()

    @memoized_property
    def covered_by_primers_alignments(self):
        ''' How much of the read is covered by alignments containing the primers? '''
        if self.strand is None:
            # primer-containing alignments mapped to opposite strands
            return None
        elif self.primer_alignments is None:
            return None
        else:
            return interval.get_disjoint_covered([self.primer_alignments[5], self.primer_alignments[3]])

    @memoized_property
    def primer_alignments_reach_edges(self):
        if self.covered_by_primers_alignments is None:
            return False
        else:
            return (self.covered_by_primers_alignments.start <= 10 and
                    len(self.seq) - self.covered_by_primers_alignments.end <= 10
                   )

    def overlaps_donor_specific(self, al):
        ti = self.target_info
        if ti.donor is None:
            return False
        elif al.reference_name != ti.donor:
            return False
        else:
            covered = interval.get_covered_on_ref(al)
            overlap = covered & ti.donor_specific_intervals
            return overlap.total_length > 0

    def overlaps_primer(self, al, side, require_correct_strand=True):
        primer = self.target_info.primers_by_side_of_read[side]
        num_overlapping_bases = al.get_overlap(primer.start, primer.end + 1)
        overlaps = num_overlapping_bases > 0
        correct_strand = sam.get_strand(al) == self.target_info.sequencing_direction 

        return overlaps and (correct_strand or not require_correct_strand)

    @memoized_property
    def any_donor_specific_present(self):
        als_to_check = self.parsimonious_and_gap_alignments
        return any(self.overlaps_donor_specific(al) for al in als_to_check)

    @memoized_property
    def single_merged_primer_alignment(self):
        ''' If the alignments from the primers are adjacent to each other on the query, merge them.
        If there is only one expected cut site, only try to perform a single merge. If there are
        more than one cut sites, merge all target alignments. '''

        primer_als = self.primer_alignments
        ref_seqs = self.target_info.reference_sequences

        if len(self.target_info.sgRNAs) <= 1:
            if primer_als[5] is not None and primer_als[3] is not None:
                merged = sam.merge_adjacent_alignments(primer_als[5], primer_als[3], ref_seqs)
            else:
                merged = None
        else:
            # If there is a single target alignment that reaches both primers (after splitting),
            # use it to avoid edge cases. 
            merged = None
            for al in self.parsimonious_target_alignments:
                if all(self.overlaps_primer(al, side, False) for side in ['left', 'right']):
                    merged = al
                    break

            if merged is None:
                merged = sam.merge_multiple_adjacent_alignments(self.parsimonious_target_alignments, ref_seqs)
                if merged is not None:
                    primers = self.target_info.primers_by_side_of_target.values()
                    # Prefer to have the primers annotated on the strand they anneal to,
                    # so don't require strand match here.
                    reaches_primers = all(sam.overlaps_feature(merged, primer, False) for primer in primers)
                    if not reaches_primers:
                        merged = None

        return merged
    
    @memoized_property
    def has_integration(self):
        covered = self.covered_by_primers_alignments
        start_covered = covered is not None and covered.start <= 10
        if not start_covered:
            return False
        else:
            if self.single_merged_primer_alignment is None:
                return True
            else:
                return False

    @memoized_property
    def mismatches_near_cut(self):
        merged_primer_al = self.single_merged_primer_alignment
        if merged_primer_al is None:
            return []
        else:
            mismatches = []
            tuples = sam.aligned_tuples(merged_primer_al, self.target_info.target_sequence)
            for true_read_i, read_b, ref_i, ref_b, qual in tuples:
                if ref_i is not None and true_read_i is not None:
                    if read_b != ref_b and ref_i in self.near_cut_intervals:
                        mismatches.append(ref_i)

            return mismatches

    @memoized_property
    def indel_near_cut(self):
        d = self.largest_deletion_near_cut
        i = self.largest_insertion_near_cut

        if d is None:
            d_length = 0
        else:
            d_length = d.length

        if i is None:
            i_length = 0
        else:
            i_length = i.length

        if d_length == 0 and i_length == 0:
            scar = None
        elif d_length > i_length:
            scar = [d]
        elif i_length > d_length:
            scar = [i]
        else:
            scar = [d, i]

        return scar

    @memoized_property
    def all_indels_near_cuts(self):
        indels_near_cuts = []
        for indel in self.indels:
            if indel.kind == 'D':
                d = indel
                d_interval = interval.Interval(min(d.starts_ats), max(d.starts_ats) + d.length - 1)
                if d_interval & self.near_cut_intervals:
                    indels_near_cuts.append(d)
            elif indel.kind == 'I':
                ins = indel
                if any(sa in self.near_cut_intervals for sa in ins.starts_afters):
                    indels_near_cuts.append(ins)

        return indels_near_cuts

    @memoized_property
    def near_cut_intervals(self):
        return self.target_info.around_cuts(10)

    @memoized_property
    def largest_deletion_near_cut(self):
        dels = [indel for indel in self.indels if indel.kind == 'D']

        near_cut = []
        for deletion in dels:
            del_interval = interval.Interval(min(deletion.starts_ats), max(deletion.starts_ats) + deletion.length - 1)
            if del_interval & self.near_cut_intervals:
                near_cut.append(deletion)

        if near_cut:
            largest = max(near_cut, key=lambda d: d.length)
            largest = self.target_info.expand_degenerate_indel(largest)
        else:
            largest = None

        return largest

    @memoized_property
    def largest_insertion_near_cut(self):
        insertions = [indel for indel in self.indels if indel.kind == 'I']

        near_cut = [ins for ins in insertions if any(sa in self.near_cut_intervals for sa in ins.starts_afters)]

        if near_cut:
            largest = max(near_cut, key=lambda ins: len(ins.seqs[0]))
            largest = self.target_info.expand_degenerate_indel(largest)
        else:
            largest = None

        return largest
    
    @memoized_property
    def indel_string(self):
        if self.indel_near_cut is None:
            indel_string = None
        else:
            indel_string = ' '.join(map(str, self.indel_near_cut))

        return indel_string

    @memoized_property
    def parsimonious_alignments(self):
        return interval.make_parsimonious(self.alignments)

    @memoized_property
    def parsimonious_and_gap_alignments(self):
        ''' identification of gap_alignments requires further processing of parsimonious alignments '''
        return sam.make_nonredundant(interval.make_parsimonious(self.parsimonious_alignments + self.sw_gap_alignments))

    @memoized_property
    def parsimonious_target_alignments(self):
        return [al for al in self.parsimonious_and_gap_alignments if al.reference_name == self.target_info.target]

    @memoized_property
    def parsimonious_donor_alignments(self):
        return [al for al in self.parsimonious_and_gap_alignments if al.reference_name == self.target_info.donor]

    @memoized_property
    def closest_donor_alignment_to_edge(self):
        ''' Identify the alignments to the donor closest to edge of the read
        that has the PAM-proximal and PAM-distal amplicon primer. '''
        donor_als = self.parsimonious_donor_alignments

        if self.strand is None or len(donor_als) == 0:
            closest = {5: None, 3: None}
        else:
            closest = {}

            left_most = min(donor_als, key=lambda al: interval.get_covered(al).start)
            right_most = max(donor_als, key=lambda al: interval.get_covered(al).end)

            if self.strand == '+':
                closest[5] = left_most
                closest[3] = right_most
            else:
                closest[5] = right_most
                closest[3] = left_most

        return closest

    @memoized_property
    def clean_handoff(self):
        ''' Check if target sequence cleanly transitions to donor sequence at
        each junction between the two, with one full length copy of the relevant
        homology arm and no large indels (i.e. not from sequencing errors) near
        the internal edge.
        '''
        if len(self.donor_alignments) == 0 or self.primer_alignments is None:
            return {5: False, 3: False}

        from_primer = self.primer_alignments
        HAs = self.target_info.homology_arms
        closest_donor = self.closest_donor_alignment_to_edge

        if closest_donor[5] is None and closest_donor[3] is None:
            return {5: False, 3: False}

        if 'donor' not in HAs[5] or 'donor' not in HAs[3]:
            # The donor doesn't share homology arms with the target.
            return {5: False, 3: False}

        target_contains_full_arm = {
            5: (HAs[5]['target'].end - from_primer[5].reference_end <= 10
                if from_primer[5] is not None else False),
            3: (from_primer[3].reference_start - HAs[3]['target'].start <= 10
                if from_primer[3] is not None else False),
        }

        donor_contains_arm_external = {
            5: closest_donor[5].reference_start - HAs[5]['donor'].start <= 10,
            3: HAs[3]['donor'].end - (closest_donor[3].reference_end - 1) <= 10,
        }

        donor_contains_arm_internal = {
            5: closest_donor[5].reference_end - 1 - HAs[5]['donor'].end >= 0,
            3: HAs[3]['donor'].start - closest_donor[3].reference_start >= 0,
        }

        donor_past_HA = {
            5: sam.crop_al_to_ref_int(closest_donor[5], HAs[5]['donor'].end + 1, np.inf),
            3: sam.crop_al_to_ref_int(closest_donor[3], 0, HAs[3]['donor'].start - 1),
        }
        
        donor_past_HA_length = {
            side: donor_past_HA[side].query_alignment_length if donor_past_HA[side] is not None else 0
            for side in [5, 3]
        }
        
        donor_past_HA_edit_distance = {
            side: sam.total_edit_distance(donor_past_HA[side], self.target_info.donor_sequence)
            for side in [5, 3]
        }

        donor_matches_past_HA = {
            side: donor_past_HA_length[side] - donor_past_HA_edit_distance[side]
            for side in [5, 3]
        }

        donor_contains_full_arm = {
            side: donor_contains_arm_external[side] and \
                  donor_contains_arm_internal[side] and \
                  (donor_matches_past_HA[side] >= 5 or (donor_past_HA_length[side] >= 2 and donor_past_HA_edit_distance[side] == 0))
            for side in [5, 3]
        }
            
        target_external_edge_query = {
            5: (sam.closest_query_position(HAs[5]['target'].start, from_primer[5])
                if from_primer[5] is not None else None),
            3: (sam.closest_query_position(HAs[3]['target'].end, from_primer[3])
                if from_primer[3] is not None else None),
        }
        
        donor_external_edge_query = {
            5: sam.closest_query_position(HAs[5]['donor'].start, closest_donor[5]),
            3: sam.closest_query_position(HAs[3]['donor'].end, closest_donor[3]),
        }

        arm_overlaps = {
            side: (abs(target_external_edge_query[side] - donor_external_edge_query[side]) <= 10
                   if target_external_edge_query[side] is not None else False)
            for side in [5, 3]
        }

        junction = {
            5: HAs[5]['donor'].end,
            3: HAs[3]['donor'].start,
        }

        max_indel_near_junction = {
            side: max_indel_nearby(closest_donor[side], junction[side], 10)
            for side in [5, 3]
        }

        clean_handoff = {}
        for side in [5, 3]:
            clean_handoff[side] = (
                target_contains_full_arm[side] and
                donor_contains_full_arm[side] and
                arm_overlaps[side] and
                max_indel_near_junction[side] <= 2
            )

        return clean_handoff
    
    @memoized_property
    def edge_q(self):
        ''' Where in the query are the edges of the integration? '''
        if self.strand == '+':
            edge_q = {
                5: self.integration_interval.start,
                3: self.integration_interval.end,
            }
        else:
            edge_q = {
                5: self.integration_interval.end,
                3: self.integration_interval.start,
            }
        return edge_q

    @memoized_property
    def edge_r(self):
        ''' Where in the donor are the edges of the integration? '''
        all_edge_rs = {
            5: [],
            3: [],
        }

        for al in self.parsimonious_donor_alignments:
            cropped = sam.crop_al_to_query_int(al, self.integration_interval.start, self.integration_interval.end)
            if cropped is None:
                continue
            start = cropped.reference_start
            end = cropped.reference_end - 1
            all_edge_rs[5].append(start)
            all_edge_rs[3].append(end)

        edge_r = {}

        if all_edge_rs[5]:
            edge_r[5] = min(all_edge_rs[5])
        else:
            edge_r[5] = None

        if all_edge_rs[3]:
            edge_r[3] = max(all_edge_rs[3])
        else:
            edge_r[3] = None

        return edge_r

    @memoized_property
    def donor_relative_to_arm(self):
        ''' How much of the donor is integrated relative to the edges of the HAs? '''
        HAs = self.target_info.homology_arms

        # convention: positive if there is extra in the integration, negative if truncated
        relative_to_arm = {
            'internal': {
                5: ((HAs[5]['donor'].end + 1) - self.edge_r[5]
                    if self.edge_r[5] is not None else None),
                3: (self.edge_r[3] - (HAs[3]['donor'].start - 1)
                    if self.edge_r[3] is not None else None),
            },
            'external': {
                5: (HAs[5]['donor'].start - self.edge_r[5]
                    if self.edge_r[5] is not None else None),
                3: (self.edge_r[3] - HAs[3]['donor'].end
                    if self.edge_r[3] is not None else None),
            },
        }

        return relative_to_arm
    
    @memoized_property
    def donor_relative_to_cut(self):
        ''' Distance on query between base aligned to donor before/after cut
        and start of target alignment.
        This doesn't appear to be used.
        '''
        to_cut = {
            5: None,
            3: None,
        }

        ti = self.target_info

        try:
            donor_edge = {
                5: ti.features[ti.donor, "5' edge"].start,
                3: ti.features[ti.donor, "3' edge"].start,
            }
        except KeyError:
            return to_cut

        for side in [5, 3]:
            if self.edge_r[side] is not None:
                to_cut[side] = self.edge_r[side] - donor_edge[side]

        return to_cut

    @memoized_property
    def donor_integration_is_blunt(self):
        donor_length = len(self.target_info.donor_sequence)

        reaches_end = {
            5: self.edge_r[5] is not None and self.edge_r[5] <= 1,
            3: self.edge_r[3] is not None and self.edge_r[3] >= donor_length - 2,
        }

        short_gap = {}
        for side in [5, 3]:
            primer_al = self.primer_alignments[side]
            donor_al = self.closest_donor_alignment_to_edge[side]
            overlap = junction_microhomology(self.target_info.reference_sequences, primer_al, donor_al)
            short_gap[side] = overlap > -10

        is_blunt = {side: reaches_end[side] and short_gap[side] for side in [5, 3]}

        return is_blunt

    @memoized_property
    def donor_integration_contains_full_HA(self):
        HAs = self.target_info.homology_arms
        if 'donor' not in HAs[5] or 'donor' not in HAs[3]:
            return {5: False, 3: False}
        if not self.has_integration:
            return {5: False, 3: False}

        full_HA = {}
        for side in [5, 3]:
            offset = self.donor_relative_to_arm['external'][side]
            
            full_HA[side] = offset is not None and offset >= 0

        return full_HA

    @memoized_property
    def integration_interval(self):
        ''' because cut site might not exactly coincide with boundary between
        HAs, the relevant part of query to call integration depends on whether
        a clean HDR handoff is detected at each edge '''
        if not self.has_integration:
            return None

        HAs = self.target_info.homology_arms
        cut_after = self.target_info.cut_after

        flanking_al = {}
        mask_start = {5: -np.inf}
        mask_end = {3: np.inf}
        for side in [5, 3]:
            if self.clean_handoff[side]:
                flanking_al[side] = self.closest_donor_alignment_to_edge[side]
            else:
                flanking_al[side] = self.primer_alignments[side]

        if self.clean_handoff[5] or cut_after is None:
            mask_end[5] = HAs[5]['donor'].end
        else:
            mask_end[5] = cut_after

        if self.clean_handoff[3] or cut_after is None:
            mask_start[3] = HAs[3]['donor'].start
        else:
            mask_start[3] = cut_after + 1

        covered = {
            side: (sam.crop_al_to_ref_int(flanking_al[side], mask_start[side], mask_end[side])
                   if flanking_al[side] is not None else None
                  )
            for side in [5, 3]
        }

        if self.strand == '+':
            if covered[5] is not None:
                start = interval.get_covered(covered[5]).end + 1
            else:
                start = 0

            if covered[3] is not None:
                end = interval.get_covered(covered[3]).start - 1
            else:
                end = len(self.seq) - 1

        elif self.strand == '-':
            if covered[5] is not None:
                end = interval.get_covered(covered[5]).start - 1
            else:
                end = len(self.seq) - 1

            if covered[3] is not None:
                start = interval.get_covered(covered[3]).end + 1
            else:
                start = 0

        return interval.Interval(start, end)

    @memoized_property
    def gap_between_primer_alignments(self):
        if self.primer_alignments[5] is None or self.primer_alignments[3] is None or self.strand is None:
            return interval.Interval.empty()

        left_covered = interval.get_covered(self.primer_alignments[5])
        right_covered = interval.get_covered(self.primer_alignments[3])
        if self.strand == '+':
            between_primers = interval.Interval(left_covered.start, right_covered.end)
        elif self.strand == '-':
            between_primers = interval.Interval(right_covered.start, left_covered.end)
        else:
            raise ValueError

        gap = between_primers - left_covered - right_covered
        
        return gap

    @memoized_property
    def target_to_at_least_cut(self):
        cut_after = self.target_info.cut_after
        primer_als = self.primer_alignments

        target_to_at_least_cut = {
            5: primer_als[5].reference_end - 1 >= cut_after,
            3: primer_als[3].reference_start <= (cut_after + 1),
        }

        return target_to_at_least_cut

    @memoized_property
    def junction_summary_per_side(self):
        per_side = {}

        for side in [5, 3]:
            if self.clean_handoff[side]:
                per_side[side] = 'HDR'
            elif self.donor_integration_is_blunt[side]:
                per_side[side] = 'blunt'
            else:
                per_side[side] = 'imperfect'

        return per_side
                
    @memoized_property
    def junction_summary(self):
        per_side = self.junction_summary_per_side

        if (per_side[5] == 'HDR' and
            per_side[3] == 'HDR'):

            summary = 'HDR'

        elif (per_side[5] == 'blunt' and
              per_side[3] == 'HDR'):

            summary = "5' blunt"
        
        elif (per_side[5] == 'HDR' and
              per_side[3] == 'blunt'):

            summary = "3' blunt"
        
        elif (per_side[5] == 'blunt' and
              per_side[3] == 'blunt'):

            summary = "5' and 3' blunt"

        else:
            summary = 'incomplete'

        # blunt isn't a meaningful concept for plasmid donors
        if self.target_info.donor_type == 'plasmid':
            if 'blunt' in summary:
                summary = 'incomplete'

        return summary

    @memoized_property
    def donor_specific_integration_alignments(self):
        integration_donor_als = []

        for al in self.parsimonious_donor_alignments:
            if self.overlaps_donor_specific(al):
                covered = interval.get_covered(al)
                if (self.integration_interval.total_length > 0) and ((self.integration_interval - covered).total_length == 0):
                    # If a single donor al covers the whole integration, use just it.
                    integration_donor_als = [al]
                    break
                else:
                    covered_integration = self.integration_interval & interval.get_covered(al)
                    # Ignore als that barely extend past the homology arms.
                    if len(covered_integration) >= 5:
                        integration_donor_als.append(al)

        return sorted(integration_donor_als, key=lambda al: al.query_alignment_length, reverse=True)

    @memoized_property
    def integration_summary(self):
        if len(self.donor_specific_integration_alignments) == 0:
            summary = 'other'

        elif len(self.donor_specific_integration_alignments) == 1:
            donor_al = self.donor_specific_integration_alignments[0]
            covered_by_donor = interval.get_covered(donor_al)
            uncovered_length = (self.integration_interval - covered_by_donor).total_length

            if uncovered_length > 10:
                summary = 'other'
            else:
                max_indel_length = sam.max_block_length(donor_al, {sam.BAM_CDEL, sam.BAM_CINS})
                if max_indel_length > self.max_indel_allowed_in_donor:
                    summary = 'donor with indel'
                else:
                    summary = 'donor'

        else:
            if self.cleanly_concatanated_donors > 1:
                summary = 'concatamer'

            else:
                #TODO: check for plasmid extensions around the boundary
                summary = 'other'

        return summary
    
    @memoized_property
    def cleanly_concatanated_donors(self):
        ti = self.target_info

        HAs = ti.homology_arms
        p_donor_als = self.parsimonious_donor_alignments

        if len(p_donor_als) <= 1:
            return 0

        # TEMPORARY
        if 'donor' not in HAs[5] or 'donor' not in HAs[3]:
            # The donor doesn't share homology arms with the target.
            return 0

        if self.strand == '+':
            key = lambda al: interval.get_covered(al).start
            reverse = False
        else:
            key = lambda al: interval.get_covered(al).end
            reverse = True

        five_to_three = sorted(p_donor_als, key=key, reverse=reverse)
        junctions_clean = []

        for before, after in zip(five_to_three[:-1], five_to_three[1:]):
            before_int = interval.get_covered(before)
            after_int = interval.get_covered(after)

            adjacent = interval.are_adjacent(before_int, after_int)
            overlap_slightly = len(before_int & after_int) <= 2

            missing_before = len(ti.donor_sequence) - before.reference_end
            missing_after = after.reference_start 

            clean = (adjacent or overlap_slightly) and (missing_before <= 1) and (missing_after <= 1)

            junctions_clean.append(clean)

        if all(junctions_clean):
            return len(junctions_clean) + 1
        else:
            return 0
    
    @memoized_property
    def indels(self):
        indels = []

        al = self.single_merged_primer_alignment

        if al is not None:
            for i, (kind, length) in enumerate(al.cigar):
                if kind == sam.BAM_CDEL:
                    nucs_before = sam.total_reference_nucs(al.cigar[:i])
                    starts_at = al.reference_start + nucs_before

                    indel = DegenerateDeletion([starts_at], length)

                elif kind == sam.BAM_CINS:
                    ref_nucs_before = sam.total_reference_nucs(al.cigar[:i])
                    starts_after = al.reference_start + ref_nucs_before - 1

                    read_nucs_before = sam.total_read_nucs(al.cigar[:i])
                    insertion = al.query_sequence[read_nucs_before:read_nucs_before + length]

                    indel = DegenerateInsertion([starts_after], [insertion])
                    
                else:
                    continue

                indels.append(indel)

        return indels

    @memoized_property
    def genomic_insertion(self):
        min_gap_length = 20
        
        covered_by_normal = interval.get_disjoint_covered(self.alignments)
        unexplained_gaps = self.whole_read - covered_by_normal

        long_unexplained_gaps = [gap for gap in unexplained_gaps if len(gap) >= min_gap_length]

        if len(long_unexplained_gaps) != 1:
            covering_als = None
        elif self.gap_alignments:
            # gap aligns to the target in the amplicon region
            covering_als = None
        else:
            gap = long_unexplained_gaps[0]

            covering_als = []
            for al in self.supplemental_alignments:
                covered = interval.get_covered(al)
                if (gap - covered).total_length <= 3:
                    edit_distance = sam.edit_distance_in_query_interval(al, gap)
                    error_rate = edit_distance / len(gap)
                    if error_rate < 0.1:
                        covering_als.append(al)
                    
            if len(covering_als) == 0:
                covering_als = None

        return covering_als

    def register_genomic_insertion(self):
        insertion_al = self.min_edit_distance_genomic_insertions[0]

        organism, original_al = self.target_info.remove_organism_from_alignment(insertion_al)

        # TODO: these need to be cropped.

        target_ref_bounds = {
            'left': sam.reference_edges(self.primer_alignments[5])[3],
            'right': sam.reference_edges(self.primer_alignments[3])[5],
        }

        insertion_ref_bounds = {
            'left': sam.reference_edges(insertion_al)[5],
            'right': sam.reference_edges(insertion_al)[3],
        }

        insertion_query_bounds = {}
        insertion_query_bounds['left'], insertion_query_bounds['right'] = sam.query_interval(insertion_al)

        outcome = knock_knock.outcome.LongTemplatedInsertionOutcome(organism,
                                                original_al.reference_name,
                                                sam.get_strand(insertion_al),
                                                insertion_ref_bounds['left'],
                                                insertion_ref_bounds['right'],
                                                insertion_query_bounds['left'],
                                                insertion_query_bounds['right'],
                                                target_ref_bounds['left'],
                                                target_ref_bounds['right'],
                                                -1,
                                                -1,
                                                -1,
                                                -1,
                                                '',
                                               )

        self.outcome = outcome

        self.category = 'genomic insertion'
        self.subcategory = organism
        self.details = str(outcome)

        alignments = self.parsimonious_and_gap_alignments + self.parsimonious_donor_alignments + self.min_edit_distance_genomic_insertions
        self.relevant_alignments = interval.make_parsimonious(alignments)

    @memoized_property
    def one_sided_covering_als(self):
        all_covering_als = {
            'nonspecific_amplification': None,
            'genomic_insertion': None,
            'h': None,
            'nh': None,
        }
        
        if self.strand == '+':
            primer_al = self.primer_alignments[5]
        elif self.strand == '-':
            primer_al = self.primer_alignments[3]
        else:
            return all_covering_als

        covered = interval.get_covered(primer_al)

        close_to_start = primer_al is not None and covered.start <= 10

        if not close_to_start:
            return all_covering_als

        # from supplementary alignments

        has_extra = self.extra_query_in_primer_als['left'] >= 20

        if has_extra:
            kind = 'genomic_insertion'
            primer_interval = interval.get_covered(primer_al)
            primer_interval.start = 0
        else:
            kind = 'nonspecific_amplification'
            primer_interval = self.just_primer_interval['left']
            
        need_to_cover = self.whole_read - primer_interval
        covering_als = []
        for supp_al in self.supplemental_alignments:
            if (need_to_cover - interval.get_covered(supp_al)).total_length <= 10:
                covering_als.append(supp_al)
                
        if covering_als:
            all_covering_als[kind] = covering_als

        # from donor and nh-donor als

        primer_interval = interval.get_covered(primer_al)
        primer_interval.start = 0
            
        need_to_cover = self.whole_read - primer_interval
        for kind, all_als in [('h', self.parsimonious_donor_alignments),
                              ('nh', self.nonhomologous_donor_alignments),
                             ]:
            covering_als = []
            for al in all_als:
                if (need_to_cover - interval.get_covered(al)).total_length <= 10:
                    covering_als.append(al)
                
            if covering_als:
                all_covering_als[kind] = covering_als

        return all_covering_als
    
    @memoized_property
    def nonhomologous_donor_integration_alignments(self):
        min_gap_length = 10
        gap = self.gap_between_primer_alignments
        
        covered_by_normal = interval.get_disjoint_covered(self.alignments)
        unexplained_gap = gap - covered_by_normal

        if unexplained_gap.total_length < min_gap_length:
            return [], []
        elif self.gap_alignments:
            # gap aligns to the target in the amplicon region
            return [], []
        else:
            full_covering_als = []
            partial_covering_als = []

            for al in self.nonhomologous_donor_alignments:
                covered = interval.get_covered(al)
                if (gap - covered).total_length <= 2:
                    full_covering_als.append(al)
                
                if (covered & unexplained_gap).total_length >= 2:
                    partial_covering_als.append(al)
                    
            return full_covering_als, partial_covering_als

    @memoized_property
    def nonhomologous_donor_integration(self):
        full_covering_als, partial_covering_als = self.nonhomologous_donor_integration_alignments
        if len(full_covering_als) > 0:
            return full_covering_als
        else:
            return None

    @memoized_property
    def partial_nonhomologous_donor_integration(self):
        full_covering_als, partial_covering_als = self.nonhomologous_donor_integration_alignments
        if self.nonhomologous_donor_integration is not None:
            return None
        elif len(partial_covering_als) == 0:
            return None
        else:
            return partial_covering_als

    @memoized_property
    def min_edit_distance_genomic_insertions(self):
        covering_als = self.genomic_insertion
        if covering_als is None:
            return None
        else:
            edit_distances = [sam.edit_distance_in_query_interval(al) for al in covering_als]
            min_distance = min(edit_distances)
            best_als = [al for al, distance in zip(covering_als, edit_distances) if distance == min_distance]
            return best_als

    @memoized_property
    def extra_query_in_primer_als(self):
        not_primer_length = {'left': 0, 'right': 0}

        if self.strand is None:
            return not_primer_length

        for target_side in [5, 3]:
            if (target_side == 5 and self.strand == '+') or (target_side == 3 and self.strand == '-'):
                read_side = 'left'
            elif (target_side == 3 and self.strand == '+') or (target_side == 5 and self.strand == '-'):
                read_side = 'right'

            al = self.primer_alignments[target_side]
            if al is None:
                not_primer_length[read_side] = 0
                continue

            not_primer_interval = self.whole_read - self.just_primer_interval[read_side]
            not_primer_al = sam.crop_al_to_query_int(al, not_primer_interval.start, not_primer_interval.end)
            if not_primer_al is None:
                not_primer_length[read_side] = 0
            else:
                not_primer_length[read_side] = not_primer_al.query_alignment_length

        return not_primer_length

    @memoized_property
    def just_primer_interval(self):
        primer_interval = {'left': None, 'right': None}

        if self.strand is None:
            return primer_interval

        for target_side in [5, 3]:
            if (target_side == 5 and self.strand == '+') or (target_side == 3 and self.strand == '-'):
                read_side = 'left'
            elif (target_side == 3 and self.strand == '+') or (target_side == 5 and self.strand == '-'):
                read_side = 'right'

            al = self.primer_alignments[target_side]
            if al is None:
                primer_interval[read_side] = None
                continue

            primer = self.target_info.primers_by_side_of_target[target_side]
            just_primer_al = sam.crop_al_to_ref_int(al, primer.start, primer.end)
            start, end = sam.query_interval(just_primer_al)
            if read_side == 'left':
                primer_interval[read_side] = interval.Interval(0, end)
            elif read_side == 'right':
                primer_interval[read_side] = interval.Interval(start, len(self.seq) - 1)

        return primer_interval

    @memoized_property
    def nonspecific_amplification(self):
        if not self.primer_alignments_reach_edges:
            return None

        not_primer_length = self.extra_query_in_primer_als
        primer_interval = self.just_primer_interval

        # If alignments from the primers extend substantially into the read,
        # don't consider this nonspecific amplification. 

        if not_primer_length['left'] >= 20 or not_primer_length['right'] >= 20:
            return None

        need_to_cover = self.whole_read - primer_interval['left'] - primer_interval['right']

        covering_als = []
        for al in self.supplemental_alignments:
            covered = interval.get_covered(al)
            if len(need_to_cover - covered) < 10:
                covering_als.append(al)
                
        if len(covering_als) == 0:
            covering_als = None
        else:
            covering_als = interval.make_parsimonious(covering_als)
            
        return covering_als

    @memoized_property
    def uncategorized_relevant_alignments(self):
        sources = [
            self.parsimonious_and_gap_alignments,
            self.nonhomologous_donor_alignments,
            self.extra_alignments,
        ]
        flattened = [al for source in sources for al in source]
        parsimonious = sam.make_nonredundant(interval.make_parsimonious(flattened))

        covered = interval.get_disjoint_covered(parsimonious)
        supp_als = []

        def novel_length(supp_al):
            return (interval.get_covered(supp_al) - covered).total_length

        supp_als = interval.make_parsimonious(self.nonredundant_supplemental_alignments)
        supp_als = sorted(supp_als, key=novel_length, reverse=True)[:10]

        final = parsimonious + supp_als

        if len(final) == 0:
            # If there aren't any real alignments, pass along unmapped alignments in
            # case visualization needs to get seq or qual from them.
            final = self.unmapped_alignments

        return final

    @memoized_property
    def templated_insertion_relevant_alignments(self):
        return sam.make_nonredundant(interval.make_parsimonious(self.parsimonious_target_alignments + self.all_target_gap_alignments))

    @memoized_property
    def donor_microhomology(self):
        if len(self.parsimonious_donor_alignments) == 1:
            donor_al = self.parsimonious_donor_alignments[0]
        else:
            donor_al = None
            
        MH_nts = {side: junction_microhomology(self.target_info.reference_sequences, self.primer_alignments[side], donor_al) for side in [5, 3]}

        return MH_nts

    @memoized_property
    def NH_donor_microhomology(self):
        if self.nonhomologous_donor_integration:
            nh_al = self.nonhomologous_donor_alignments[0]
        else:
            nh_al = None

        MH_nts = {side: junction_microhomology(self.target_info.reference_sequences, self.primer_alignments[side], nh_al) for side in [5, 3]}

        return MH_nts

    def plot(self, relevant=True, manual_alignments=None, **manual_diagram_kwargs):
        label_overrides = {}
        label_offsets = {}
        feature_heights = {}

        if relevant and not self.categorized:
            self.categorize()

        ti = self.target_info
        features_to_show = {*ti.features_to_show}

        flip_target = ti.sequencing_direction == '-'

        for name in ti.protospacer_names:
            label_overrides[name] = 'protospacer'
            label_offsets[name] = 1

        label_overrides.update({feature_name: None for feature_name in ti.PAM_features})

        features_to_show.update({(ti.target, name) for name in ti.protospacer_names})
        features_to_show.update({(ti.target, name) for name in ti.PAM_features})

        diagram_kwargs = dict(
            draw_sequence=True,
            flip_target=flip_target,
            split_at_indels=True,
            features_to_show=features_to_show,
            label_offsets=label_offsets,
            label_overrides=label_overrides,
            inferred_amplicon_length=self.inferred_amplicon_length,
            center_on_primers=True,
            highlight_SNPs=True,
            feature_heights=feature_heights,
            layout_mode=self.mode,
        )

        for k, v in diagram_kwargs.items():
            manual_diagram_kwargs.setdefault(k, v)

        if manual_alignments is not None:
            als_to_plot = manual_alignments
        elif relevant:
            als_to_plot = self.relevant_alignments
        else:
            als_to_plot = self.alignments

        diagram = knock_knock.visualize.ReadDiagram(als_to_plot,
                                                    ti,
                                                    **manual_diagram_kwargs,
                                                   )

        return diagram

class NonoverlappingPairLayout():
    def __init__(self, R1_als, R2_als, target_info):
        self.target_info = target_info
        self.layouts = {
            'R1': Layout(R1_als, target_info, mode='illumina'),
            'R2': Layout(R2_als, target_info, mode='illumina'),
        }
        if self.layouts['R1'].name != self.layouts['R2'].name:
            raise ValueError
        
        self.name = self.layouts['R1'].name
        self.query_name = self.name

    @memoized_property
    def bridging_alignments(self):
        bridging_als = {
            'h': {'R1': None, 'R2': None},
            'nh': {'R1': None, 'R2': None},
        }
        
        for which in ['R1', 'R2']:
            if self.layouts[which].has_integration:
                for kind in ['h', 'nh']:
                    als = self.layouts[which].one_sided_covering_als[kind]
                    if als is not None and len(als) == 1:
                        bridging_als[kind][which] = als[0]

        bridging_als.update(self.best_genomic_al_pairs)
        
        return bridging_als

    @memoized_property
    def target_sides(self):
        target_sides = {}

        for which in ['R1', 'R2']:
            primer_als = self.layouts[which].primer_alignments
            sides = set(s for s, al in primer_als.items() if al is not None)
            if len(sides) == 1:
                side = sides.pop()
            else:
                side = None

            target_sides[which] = side

        return target_sides

    @memoized_property
    def strand(self):
        if self.target_sides['R1'] == 5 and self.target_sides['R2'] == 3:
            strand = '+'
        elif self.target_sides['R2'] == 5 and self.target_sides['R1'] == 3:
            strand = '-'
        else:
            strand = None
        return strand

    @memoized_property
    def best_genomic_al_pairs(self):
        best_pairs = {}
        for kind in ['nonspecific_amplification', 'genomic_insertion']:
            best_pairs[kind] = {'R1': None, 'R2': None}
            
            als = {which: self.layouts[which].one_sided_covering_als[kind] for which in ['R1', 'R2']}
            if als['R1'] is None or als['R2'] is None:
                continue
                
            valid_pairs = {}
            for R1_al, R2_al in itertools.product(als['R1'], als['R2']):
                if R1_al.reference_name != R2_al.reference_name:
                    continue

                if sam.get_strand(R1_al) == '+':
                    if sam.get_strand(R2_al) != '-':
                        # should be in opposite orientation if concordant
                        continue
                    start = R1_al.reference_start
                    end = R2_al.reference_end
                elif sam.get_strand(R1_al) == '-':
                    if sam.get_strand(R2_al) != '+':
                        continue
                    start = R2_al.reference_start
                    end = R1_al.reference_end

                length = end - start

                if 0 < length < 2000:
                    # Note: multiple valid pairs with same length are discarded.
                    valid_pairs[length] = {'R1': R1_al, 'R2': R2_al}

            if valid_pairs:
                length = min(valid_pairs)

                best_pairs[kind] = valid_pairs[length]
                
        return best_pairs

    def register_genomic_insertion(self):
        als = self.best_genomic_al_pairs['genomic_insertion']

        R1_al = als['R1']
        R2_al = als['R2']

        organism, original_al = self.target_info.remove_organism_from_alignment(R1_al)

        # TODO: these need to be cropped.

        target_ref_bounds = {
            'left': sam.reference_edges(self.layouts['R1'].primer_alignments[5])[3],
            'right': sam.reference_edges(self.layouts['R2'].primer_alignments[3])[3],
        }

        insertion_ref_bounds = {
            'left': sam.reference_edges(R1_al)[5],
            'right': sam.reference_edges(R2_al)[5],
        }

        insertion_query_bounds = {
            'left': sam.query_interval(R1_al)[0],
            'right': self.inferred_amplicon_length - 1 - sam.query_interval(R2_al)[0],
        }

        outcome = knock_knock.outcome.LongTemplatedInsertionOutcome(organism,
                                                original_al.reference_name,
                                                sam.get_strand(R1_al),
                                                insertion_ref_bounds['left'],
                                                insertion_ref_bounds['right'],
                                                insertion_query_bounds['left'],
                                                insertion_query_bounds['right'],
                                                target_ref_bounds['left'],
                                                target_ref_bounds['right'],
                                                -1,
                                                -1,
                                                -1,
                                                -1,
                                                '',
                                               )

        self.outcome = outcome

        self.category = 'genomic insertion'
        self.subcategory = organism
        self.details = str(outcome)

    def register_nonspecific_amplification(self):
        als = self.best_genomic_al_pairs['nonspecific_amplification']

        al = als['R1']

        organism, original_al = self.target_info.remove_organism_from_alignment(al)

        self.category = 'nonspecific amplification'
        self.subcategory = organism
        self.details = 'n/a'

    @memoized_property
    def bridging_als_missing_from_end(self):
        missing = {k: {'R1': None, 'R2': None} for k in self.bridging_alignments}

        for kind in self.bridging_alignments:
            for which in ['R1', 'R2']:
                al = self.bridging_alignments[kind][which]
                if al is not None:
                    covered = interval.get_covered(al)
                    missing[kind][which] = len(self.layouts[which].seq) - 1 - covered.end

        return missing

    @memoized_property
    def bridging_als_reach_internal_edges(self):
        missing = self.bridging_als_missing_from_end
        reach_edges = {}
        for kind in self.bridging_alignments:
            reach_edges[kind] = all(m is not None and m <= 5 for m in missing[kind].values())

        return reach_edges

    @memoized_property
    def junctions(self):
        junctions = {
            'R1': 'uncategorized',
            'R2': 'uncategorized',
            5: 'uncategorized',
            3: 'uncategorized',
        }

        for side in ['R1', 'R2']:
            target_side = self.target_sides.get(side)
            if target_side is not None:
                junction = self.layouts[side].junction_summary_per_side[target_side]
                junctions[side] = junction
                junctions[target_side] = junction

        return junctions

    @property
    def possible_inferred_amplicon_length(self):
        length = len(self.layouts['R1'].seq) + len(self.layouts['R2'].seq) + self.gap
        return length

    @memoized_property
    def bridging_strand(self):
        strand = {}
        for kind in self.bridging_alignments:
            strand[kind] = None
            
            als = self.bridging_alignments[kind]
            if als['R1'] is None or als['R2'] is None:
                continue

            # Note: R2 should be opposite orientation as R1
            flipped_als = [als['R1'], sam.flip_alignment(als['R2'])]
            strands = {sam.get_strand(al) for al in flipped_als}
            if len(strands) > 1:
                continue
            else:
                strand[kind] = strands.pop()

        return strand

    @memoized_property
    def successful_bridging_kind(self):
        successful = set()
        
        for kind in self.bridging_alignments:
            if self.bridging_strand[kind] is not None and self.bridging_als_reach_internal_edges[kind]:
                successful.add(kind)

                
        if len(successful) == 0:
            return None
        elif len(successful) > 1:
            if 'h' in successful:
                return 'h'
            else:
                raise ValueError(self.name, successful)
        else:
            return successful.pop()
    
    @memoized_property
    def gap(self):
        kind = self.successful_bridging_kind
        if kind is None:
            return 100
        
        als = self.bridging_alignments[kind]
        unaligned_gap = sum(self.bridging_als_missing_from_end[kind].values())
        if self.bridging_strand[kind] == '+':
            # If there is no gap, R1 reference_end (which points one past actual end)
            # will be the same as R2 reference_start.
            aligned_gap = als['R2'].reference_start - als['R1'].reference_end
        elif self.bridging_strand[kind] == '-':
            aligned_gap = als['R1'].reference_start - als['R2'].reference_end

        return aligned_gap - unaligned_gap

    @memoized_property
    def uncategorized_relevant_alignments(self):
        als = {which: l.uncategorized_relevant_alignments for which, l in self.layouts.items()}

        return als

    def categorize(self):
        kind = self.successful_bridging_kind
        if kind == 'h' and self.possible_inferred_amplicon_length > 0:
            self.inferred_amplicon_length = self.possible_inferred_amplicon_length

            self.relevant_alignments = {
                'R1': self.layouts['R1'].parsimonious_target_alignments + self.layouts['R1'].parsimonious_donor_alignments,
                'R2': self.layouts['R2'].parsimonious_target_alignments + self.layouts['R2'].parsimonious_donor_alignments,
            }

            junctions = set(self.junctions.values())

            if 'blunt' in junctions and 'uncategorized' not in junctions:
                self.category = 'blunt misintegration'
                self.subcategory = f'5\' {self.junctions[5]}, 3\' {self.junctions[3]}'
                self.details = 'n/a'
            elif junctions == set(['imperfect', 'HDR']):
                self.category = 'incomplete HDR'
                self.subcategory = f'5\' {self.junctions[5]}, 3\' {self.junctions[3]}'
                self.details = 'n/a'
            elif junctions == set(['imperfect']):
                self.category = 'complex misintegration'
                self.subcategory = 'complex misintegration'
                self.details = 'n/a'

            else:
                self.inferred_amplicon_length = -1
                self.category = 'bad sequence'
                self.subcategory = 'non-overlapping'
                self.details = 'n/a'
                self.relevant_alignments = self.uncategorized_relevant_alignments

        elif kind == 'nh' and self.possible_inferred_amplicon_length > 0:
            self.inferred_amplicon_length = self.possible_inferred_amplicon_length

            self.category = 'non-homologous donor'
            self.subcategory = 'simple'
            self.details = 'n/a'
            self.relevant_alignments = {
                'R1': self.layouts['R1'].parsimonious_target_alignments + self.layouts['R1'].nonhomologous_donor_alignments,
                'R2': self.layouts['R2'].parsimonious_target_alignments + self.layouts['R2'].nonhomologous_donor_alignments,
            }
            
        elif kind == 'nonspecific_amplification' and self.possible_inferred_amplicon_length > 0:
            R1_primer = self.layouts['R1'].primer_alignments[5]
            R2_primer = self.layouts['R2'].primer_alignments[3]

            if R1_primer is not None and R2_primer is not None:
                self.inferred_amplicon_length = self.possible_inferred_amplicon_length

                self.register_nonspecific_amplification()

                bridging_als = self.bridging_alignments['nonspecific_amplification']
                self.relevant_alignments = {
                    'R1': [R1_primer, bridging_als['R1']],
                    'R2': [R2_primer, bridging_als['R2']],
                }

            else:
                self.inferred_amplicon_length = -1
                self.category = 'bad sequence'
                self.subcategory = 'non-overlapping'
                self.details = 'n/a'
                self.relevant_alignments = self.uncategorized_relevant_alignments
        
        elif kind == 'genomic_insertion' and self.possible_inferred_amplicon_length > 0:
            R1_primer = self.layouts['R1'].primer_alignments[5]
            R2_primer = self.layouts['R2'].primer_alignments[3]

            if R1_primer is not None and R2_primer is not None:
                self.inferred_amplicon_length = self.possible_inferred_amplicon_length

                self.register_genomic_insertion()

                bridging_als = self.bridging_alignments['genomic_insertion']
                self.relevant_alignments = {
                    'R1': [R1_primer, bridging_als['R1']],
                    'R2': [R2_primer, bridging_als['R2']],
                }
            else:
                self.inferred_amplicon_length = -1
                self.category = 'bad sequence'
                self.subcategory = 'non-overlapping'
                self.details = 'n/a'
                self.relevant_alignments = self.uncategorized_relevant_alignments
            
        else:
            self.inferred_amplicon_length = -1
            self.category = 'bad sequence'
            self.subcategory = 'non-overlapping'
            self.details = 'n/a'
            self.relevant_alignments = self.uncategorized_relevant_alignments
        
        #if self.strand == '-':
        #    self.relevant_alignments = {
        #        'R1': self.relevant_alignments['R2'],
        #        'R2': self.relevant_alignments['R1'],
        #    }
            
        return self.category, self.subcategory, self.details
    
def max_del_nearby(alignment, ref_pos, window):
    ref_pos_to_block = sam.get_ref_pos_to_block(alignment)
    nearby = range(ref_pos - window, ref_pos + window)
    blocks = [ref_pos_to_block.get(r, (-1, -1, -1)) for r in nearby]
    dels = [l for k, l, s in blocks if k == sam.BAM_CDEL]
    if dels:
        max_del = max(dels)
    else:
        max_del = 0

    return max_del

def max_ins_nearby(alignment, ref_pos, window):
    nearby = sam.crop_al_to_ref_int(alignment, ref_pos - window, ref_pos + window)
    max_ins = sam.max_block_length(nearby, {sam.BAM_CINS})
    return max_ins

def max_indel_nearby(alignment, ref_pos, window):
    max_del = max_del_nearby(alignment, ref_pos, window)
    max_ins = max_ins_nearby(alignment, ref_pos, window)
    return max(max_del, max_ins)

def get_mismatch_info(alignment, reference_sequences):
    mismatches = []

    tuples = []
    if reference_sequences.get(alignment.reference_name) is None:
        for read_p, ref_p, ref_b in alignment.get_aligned_pairs(with_seq=True):
            if read_p != None and ref_p != None:
                read_b = alignment.query_sequence[read_p]
                tuples.append((read_p, read_b, ref_p, ref_b))

    else:
        reference = reference_sequences[alignment.reference_name]
        for read_p, ref_p in alignment.get_aligned_pairs():
            if read_p != None and ref_p != None:
                read_b = alignment.query_sequence[read_p]
                ref_b = reference[ref_p]
                
                tuples.append((read_p, read_b, ref_p, ref_b))

    for read_p, read_b, ref_p, ref_b in tuples:
        read_b = read_b.upper()
        ref_b = ref_b.upper()

        if read_b != ref_b:
            true_read_p = sam.true_query_position(read_p, alignment)
            q = alignment.query_qualities[read_p]

            if alignment.is_reverse:
                read_b = utilities.reverse_complement(read_b)
                ref_b = utilities.reverse_complement(ref_b)

            mismatches.append((true_read_p, read_b, ref_p, ref_b, q))

    return mismatches

def get_indel_info(alignment):
    indels = []
    for i, (kind, length) in enumerate(alignment.cigar):
        if kind == sam.BAM_CDEL or kind == sam.BAM_CREF_SKIP:
            if kind == sam.BAM_CDEL:
                name = 'deletion'
            else:
                name = 'splicing'

            nucs_before = sam.total_read_nucs(alignment.cigar[:i])
            centered_at = np.mean([sam.true_query_position(p, alignment) for p in [nucs_before - 1, nucs_before]])

            indels.append((name, (centered_at, length)))

        elif kind == sam.BAM_CINS:
            # Note: edges are both inclusive.
            first_edge = sam.total_read_nucs(alignment.cigar[:i])
            second_edge = first_edge + length - 1
            starts_at, ends_at = sorted(sam.true_query_position(p, alignment) for p in [first_edge, second_edge])
            indels.append(('insertion', (starts_at, ends_at)))

    return indels

def edit_positions(al, reference_sequences, use_deletion_length=False):
    bad_read_ps = np.zeros(al.query_length)
    
    for read_p, *rest in get_mismatch_info(al, reference_sequences):
        bad_read_ps[read_p] += 1
        
    for indel_type, indel_info in get_indel_info(al):
        if indel_type == 'deletion':
            centered_at, length = indel_info
            for offset in [-0.5, 0.5]:
                if use_deletion_length:
                    to_add = length / 2
                else:
                    to_add = 1
                bad_read_ps[int(centered_at + offset)] += to_add
        elif indel_type == 'insertion':
            starts_at, ends_at = indel_info
            # TODO: double-check possible off by one in ends_at
            for read_p in range(starts_at, ends_at + 1):
                bad_read_ps[read_p] += 1
               
    return bad_read_ps

def split_at_edit_clusters(al, reference_sequences, num_edits=5, window_size=11):
    ''' Identify read locations at which there are at least num_edits edits in a windows_size nt window. 
    Excise outwards from any such location until reaching a stretch of 5 exact matches.
    Remove the excised region, producing new cropped alignments.
    '''
    split_als = []
    
    bad_read_ps = edit_positions(al, reference_sequences)
    rolling_sums = pd.Series(bad_read_ps).rolling(window=window_size, center=True, min_periods=1).sum()

    argmax = rolling_sums.idxmax()

    if rolling_sums[argmax] < num_edits:
        split_als.append(al)
    else:
        last_read_p_in_before = None
    
        window_edge = argmax
        for window_edge in range(argmax, -1, -1):
            errors_in_window_before = sum(bad_read_ps[window_edge + 1 - 5:window_edge + 1])
            if errors_in_window_before == 0:
                last_read_p_in_before = window_edge
                break
            
        if last_read_p_in_before is not None:
            cropped_before = sam.crop_al_to_query_int(al, 0, last_read_p_in_before)
            if cropped_before is not None:
                split_als.extend(split_at_edit_clusters(cropped_before, reference_sequences))

        first_read_p_in_after = None
            
        window_edge = argmax
        for window_edge in range(argmax, al.query_length):
            errors_in_window_after = sum(bad_read_ps[window_edge:window_edge + 5])
            if errors_in_window_after == 0:
                first_read_p_in_after = window_edge
                break

        if first_read_p_in_after is not None:
            cropped_after = sam.crop_al_to_query_int(al, first_read_p_in_after, np.inf)
            if cropped_after is not None:
                split_als.extend(split_at_edit_clusters(cropped_after, reference_sequences))

    split_als = [al for al in split_als if not al.is_unmapped]

    return split_als

def crop_terminal_mismatches(al, reference_sequences):
    ''' Remove all consecutive mismatches from the start and end of an alignment. '''
    covered = interval.get_covered(al)

    mismatch_ps = {p for p, *rest in knock_knock.layout.get_mismatch_info(al, reference_sequences)}

    first = covered.start
    last = covered.end

    while first in mismatch_ps:
        first += 1
        
    while last in mismatch_ps:
        last -= 1

    cropped_al = sam.crop_al_to_query_int(al, first, last)

    return cropped_al

def comprehensively_split_alignment(al, target_info, mode, ins_size_to_split_at=None, del_size_to_split_at=None):
    ''' It is easier to reason about alignments if any that contain long insertions, long deletions, or clusters
    of many edits are split into multiple alignments.
    '''

    split_als = []

    if mode == 'illumina':
        if ins_size_to_split_at is None:
            ins_size_to_split_at = 3
        
        if del_size_to_split_at is None:
            del_size_to_split_at = 1

        for split_1 in split_at_edit_clusters(al, target_info.reference_sequences):
            for split_2 in sam.split_at_deletions(split_1, del_size_to_split_at):
                for split_3 in sam.split_at_large_insertions(split_2, ins_size_to_split_at):
                    cropped_al = crop_terminal_mismatches(split_3, target_info.reference_sequences)
                    if cropped_al is not None and cropped_al.query_alignment_length >= 5:
                        split_als.append(cropped_al)

    elif mode == 'pacbio':
        # Empirically, for Pacbio data, it is hard to find a threshold for number of edits within a window that
        # doesn't produce a lot of false positive splits, so don't try to split at edit clusters.

        if ins_size_to_split_at is None:
            ins_size_to_split_at = 5
        
        if del_size_to_split_at is None:
            del_size_to_split_at = 3

        if al.reference_name == target_info.target:
            # First split at short indels close to expected cuts.
            exempt = target_info.not_around_cuts(50)
            for split_1 in sam.split_at_deletions(al, del_size_to_split_at, exempt_if_overlaps=exempt):
                for split_2 in sam.split_at_large_insertions(split_1, ins_size_to_split_at, exempt_if_overlaps=exempt):
                    # Then at longer indels anywhere.
                    for split_3 in sam.split_at_deletions(split_2, 10):
                        for split_4 in sam.split_at_large_insertions(split_3, 10):
                            split_als.append(split_4)
        else:
            for split_1 in sam.split_at_deletions(al, del_size_to_split_at):
                for split_2 in sam.split_at_large_insertions(split_1, ins_size_to_split_at):
                    split_als.append(split_2)

    else:
        raise ValueError(mode)

    return split_als

def junction_microhomology(reference_sequences, first_al, second_al):
    if first_al is None or second_al is None:
        return -1

    als_by_order = {
        'first': first_al,
        'second': second_al,
    }
    
    covered_by_order = {order: interval.get_covered(al) for order, al in als_by_order.items()}
    
    side_to_order = {
        'left': min(covered_by_order, key=covered_by_order.get),
        'right': max(covered_by_order, key=covered_by_order.get),
    }

    covered_by_side = {side: covered_by_order[order] for side, order in side_to_order.items()}
    als_by_side = {side: als_by_order[order] for side, order in side_to_order.items()}
    
    initial_overlap = covered_by_side['left'] & covered_by_side['right']

    if initial_overlap:
        # Trim back mismatches or indels in or near the overlap.
        mismatch_buffer_length = 5

        bad_read_ps = {
            'left': set(),
            'right': set(),
        }

        for side in ['left', 'right']:
            al = als_by_side[side]

            for read_p, *rest in get_mismatch_info(al, reference_sequences):
                bad_read_ps[side].add(read_p)

            for kind, info in get_indel_info(al):
                if kind == 'deletion':
                    read_p, length = info
                    bad_read_ps[side].add(read_p)
                elif kind == 'insertion':
                    starts_at, ends_at = info
                    bad_read_ps[side].update([starts_at, ends_at])

        covered_by_side_trimmed = {}

        left_buffer_start = initial_overlap.start - mismatch_buffer_length

        left_illegal_ps = [p for p in bad_read_ps['left'] if p >= left_buffer_start]

        if left_illegal_ps:
            old_start = covered_by_side['left'].start
            new_end = int(np.floor(min(left_illegal_ps))) - 1
            covered_by_side_trimmed['left'] = interval.Interval(old_start, new_end)
        else:
            covered_by_side_trimmed['left'] = covered_by_side['left']

        right_buffer_end = initial_overlap.end + mismatch_buffer_length

        right_illegal_ps = [p for p in bad_read_ps['right'] if p <= right_buffer_end]

        if right_illegal_ps:
            new_start = int(np.ceil(max(right_illegal_ps))) + 1
            old_end = covered_by_side['right'].end
            covered_by_side_trimmed['right'] = interval.Interval(new_start, old_end)
        else:
            covered_by_side_trimmed['right'] = covered_by_side['right']
    else:
        covered_by_side_trimmed = {side: covered_by_side[side] for side in ['left', 'right']}

    if interval.are_disjoint(covered_by_side_trimmed['left'], covered_by_side_trimmed['right']):
        gap = covered_by_side_trimmed['right'].start - covered_by_side_trimmed['left'].end - 1
        MH_nts = -gap
    else:   
        overlap = covered_by_side_trimmed['left'] & covered_by_side_trimmed['right']

        MH_nts = overlap.total_length

    return MH_nts