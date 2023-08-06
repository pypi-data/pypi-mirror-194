import re
import io
import xml.etree.ElementTree as ET

import PIL
import matplotlib
if 'inline' not in matplotlib.get_backend():
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

before_svg_template = '''\
<head>
<title>{title}</title>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

<style>
.popover {{
    max-width: 100%;
}}
</style>

</head>
<body>
<div style="height:5000px;text-align:center">\
'''.format

after_svg = '''\
</div>
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>

<script>
    $(document).ready(function(){
        $('[id^=length_range]').hide();

        $('[data-toggle="popover"]').popover();

        $('[data-toggle="popover"]').on('show.bs.popover', function() {
          $("path", this).attr('stroke-opacity', '0.5');
        });

        $('[data-toggle="popover"]').on('hide.bs.popover', function() {
          $("path", this).attr('stroke-opacity', '0.0');
        });
    });

    document.onkeydown = function(evt) {
        evt = evt || window.event;
        if (evt.keyCode == 27) {
            $('[data-toggle="popover"').popover('hide')
            $('[id^=length_range]').hide();

            $('[id^=outcome_category]').find('path').css('stroke-opacity', '1');

            $('[id^=line_highlighted]').find('path').css('stroke-width', '1');
            $('[id^=line_nonhighlighted]').find('path').css('stroke-width', '1');

            $('[id^=line_highlighted]').find('path').css('stroke-opacity', '1');
            $('[id^=line_nonhighlighted_6]').find('path').css('stroke-opacity', '0.6');
            $('[id^=line_nonhighlighted_3]').find('path').css('stroke-opacity', '0.3');
            $('[id^=line_nonhighlighted_05]').find('path').css('stroke-opacity', '0.05');
        }
    };
</script>

</body>\
'''
toggle_function_template = '''\
javascript:(function(){{
    $all_ranges = $('[id^=length_range]');
    $clicked_ranges = $('[id^=length_range_{outcome_string}]');

    $all_ranges.hide();
    $clicked_ranges.show();

    $all_lines = $('[id^=line_highlighted], [id^=line_nonhighlighted]').find('path');

    $all_lines.css({{
        'stroke-width': '1',
        'stroke-opacity': '0.3'
    }});

    /* For lines with initial opacity below 0.3, keep them below 0.3. */
    $('[id^=line_nonhighlighted_05]').find('path').css('stroke-opacity', '0.05');

    $clicked_lines = $('[id^=line_highlighted_{outcome_string}]').find('path');
    $clicked_lines.css({{
        'stroke-width': '2',
        'stroke-opacity': '1'
    }});

    $('[id^=outcome_category]').find('path').css('stroke-opacity', '0.5');
    $('[id^=outcome_{outcome_string}]').find('path').css('stroke-opacity', '1');

}} )();'''.format

toggle_zoom_function_template = '''\
javascript:(function(){{
    /* axes are id'd starting with axes_1 */

    $next_ax = $('#axes_' + ({panel_i} + 1 + 1));
    $next_lines = $('[id^=zoom_dotted_line_' + {panel_i} + ']');
    $next_text = $('#help_message_bracket_' + ({panel_i} + 1 + 1));

    if ($next_ax.css('visibility') == 'hidden') {{
        $next_ax.css('visibility', 'visible');
        $next_lines.css('visibility', 'visible');
        if ($('#help_message_bracket_1').css('visibility') == 'visible') {{
            $next_text.css('visibility', 'visible');
        }}
    }} else {{
        $next_ax.css('visibility', 'hidden');
        $next_lines.css('visibility', 'hidden');
        $next_text.css('visibility', 'hidden');
    }};

    for (i = {panel_i} + 1 + 1; i < {num_panels}; i++) {{
        $ax = $('#axes_' + (i + 1));
        $lines = $('[id^=zoom_dotted_line_' + (i - 1) + ']');
        $text = $('#help_message_bracket_' + (i + 1));
        $ax.css('visibility', 'hidden');
        $lines.css('visibility', 'hidden');
        $text.css('visibility', 'hidden');
    }};
}} )();'''.format

toggle_help = '''\
javascript:(function(){
    $button = $('#help_toggle path');
    if ($button.css('opacity') ==  0.2) {
        $button.css('opacity', 0.5);
    } else {
        $button.css('opacity', 0.2);
    }

    $('[id^=help_message_bracket]').each(function() {
        if ($(this).css('visibility') == 'hidden') {
            $ax = $('#axes_' + $(this).attr('id').substr(-1));
            if ($ax.css('visibility') == 'visible') {
                $(this).css('visibility', 'visible');
            }
        } else {
            $(this).css('visibility', 'hidden');
        }
    });
    $('[id^=help_message_legend]').each(function() {
        if ($(this).css('visibility') == 'hidden') {
            $(this).css('visibility', 'visible');
        } else {
            $(this).css('visibility', 'hidden');
        }
    });
} )();'''

def decorate_outcome_browser(exp, min_total_to_label=0.1):
    import knock_knock.table

    fig = exp.plot_outcome_stratified_lengths(min_total_to_label=min_total_to_label)
    num_panels = len(fig.axes)

    # Write matplotlib svg to a string.
    with io.StringIO() as write_fh:
        fig.savefig(write_fh, format='svg', bbox_inches='tight')
        contents = write_fh.getvalue()

    plt.close(fig)    

    # Read matplotib svg into an ElementTree.
    with io.StringIO(contents) as read_fh:
        d = ET.parse(read_fh)

    # ElementTree's handling of namespaces is confusing.
    # Learned this approach from http://blog.tomhennigan.co.uk/post/46945128556/elementtree-and-xmlns
    # but don't really understand it.

    default_namespace = 'http://www.w3.org/2000/svg'
    xlink_namespace = 'http://www.w3.org/1999/xlink'
    namespaces = {
        '': default_namespace,
        'xlink': xlink_namespace,
    }

    for prefix, uri in namespaces.items():
        ET.register_namespace(prefix, uri)

    elements_to_decorate = {
        'length_range': [],
        'outcome': [],
        'zoom_toggle_top': [],
        'help_toggle': [],
    }

    for element in d.iter(f'{{{default_namespace}}}g'):
        if 'id' in element.attrib:
            match = re.match('axes_(?P<panel_i_plus_one>\d+)', element.attrib['id'])
            if match:
                panel_i = int(match.group('panel_i_plus_one')) - 1
                if panel_i > 0:
                    element.attrib['style'] = 'visibility: hidden'
            
            for pattern in ['zoom_dotted_line', 'help_message']:
                match = re.match(pattern, element.attrib['id'])
                if match:
                    element.attrib['style'] = 'visibility: hidden'
            
            for prefix in elements_to_decorate:
                if element.attrib['id'].startswith(prefix):
                    elements_to_decorate[prefix].append(element)

    def decorate_with_popover(group, container_selector='body', inline_images=False):
        path = group.find(f'{{{default_namespace}}}path', namespaces)
        path.attrib.update({
            'style': 'fill:#000000;stroke:#000000;stroke-linejoin:miter;',
            'fill-opacity': '0.00',
            'stroke-opacity': '0.00',
        })
        
        match = re.match('length_range_(?P<outcome>.+)_(?P<start>\d+)_(?P<end>\d+)', group.attrib['id'])
        
        sanitized_outcome, start, end = match.groups()

        if sanitized_outcome == 'all':
            fns = exp.fns
        else:
            outcome = exp.categorizer.sanitized_string_to_outcome(sanitized_outcome)
            fns = exp.outcome_fns(outcome)

        fn = fns['length_range_figure'](start, end)

        if fn.exists() or not inline_images:
            if inline_images:
                URI, width, height = knock_knock.table.fn_to_URI(fn)
            else:
                relative_path = fn.relative_to(exp.fns['results_dir'])
                URI = str(relative_path)
                if fn.exists():
                    with PIL.Image.open(fn) as im:
                        width, height = im.size
                else:
                    width, height = 100, 100

            width = width * 0.75
            height = height * 0.75

            attrib = {
                'data-toggle': 'popover',
                'data-container': container_selector,
                'data-trigger': 'hover click',
                'data-html': 'true',
                'data-placement': 'bottom',
                'data-content': f'<img width={width} height={height} src={URI}>',
            }

            decorator = ET.Element(f'{{{default_namespace}}}a', attrib=attrib)
            decorator.append(path)
            group.remove(path)
            group.append(decorator)

    def decorate_with_toggle(group):
        path = group.find(f'{{{default_namespace}}}path', namespaces)
        
        match = re.match('outcome_(?P<outcome>.+)', group.attrib['id'])
        outcome_string = match.group('outcome')
        
        attrib = {
            f'{{{xlink_namespace}}}href': toggle_function_template(outcome_string=outcome_string),
        }
        
        decorator = ET.Element(f'{{{default_namespace}}}a', attrib=attrib)
        decorator.append(path)
        group.remove(path)
        group.append(decorator)
    
    def decorate_with_zoom_toggle(group):
        path = group.find(f'{{{default_namespace}}}path', namespaces)
        
        match = re.match('zoom_toggle_top_(?P<panel_i>.+)', group.attrib['id'])
        panel_i = match.group('panel_i')
        
        attrib = {
            f'{{{xlink_namespace}}}href': toggle_zoom_function_template(panel_i=panel_i, num_panels=num_panels),
        }
        
        decorator = ET.Element(f'{{{default_namespace}}}a', attrib=attrib)
        decorator.append(path)
        group.remove(path)
        group.append(decorator)
    
    def decorate_with_help_toggle(group):
        path = group.find(f'{{{default_namespace}}}path', namespaces)
        if path is None:
            # The question mark is deeper in the element tree.
            path = group.find(f'{{{default_namespace}}}g', namespaces)
        
        attrib = {
            f'{{{xlink_namespace}}}href': toggle_help,
        }
        
        decorator = ET.Element(f'{{{default_namespace}}}a', attrib=attrib)
        decorator.append(path)
        group.remove(path)
        group.append(decorator)

    for group in elements_to_decorate['length_range']:
        decorate_with_popover(group)
        
    for group in elements_to_decorate['outcome']:
        decorate_with_toggle(group)
    
    for group in elements_to_decorate['zoom_toggle_top']:
        decorate_with_zoom_toggle(group)
    
    for group in elements_to_decorate['help_toggle']:
        decorate_with_help_toggle(group)

    with exp.fns['outcome_browser'].open('w') as fh:
        fh.write(before_svg_template(title=exp.sample_name))
        d.write(fh, encoding='unicode')
        fh.write(after_svg)