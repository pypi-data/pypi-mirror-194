"""
Provide Graphic to show curation

Curation for price transparency isn't straight forward since unlike other raw source which have
schema on read from one logical schema, in-network-files have three schemas within the same directory and no schema
on-read serde to have a logical table.

For explainability, this visual is included with the library which will be helpful for introduction to the framework.
"""

def get_curate_html(cat_name='main'):
    import re
    from graphviz import Digraph

    dot = Digraph('pt')
    dot.attr(compound='true')
    dot.graph_attr['rankdir'] = 'LR'
    dot.edge_attr.update(arrowhead='none', arrowsize='2')
    dot.attr('node', shape='rectangle')

    def tbl_link(wh_name, tbl_name, ttip=''):
        return {'tooltip': ttip, 'href': f'./explore/data/{cat_name}/{wh_name}/{tbl_name}', 'target': "_blank"}

    with dot.subgraph(name='cluster_workflow') as c:
        c.body.append('label="Price Transparency: In-Network Workflow"')
        with c.subgraph(name='cluster_pt_raw') as r:
            r.body.append('label="pt_raw"')
            r.body.append('style="filled"')
            r.body.append('color="#808080"')
            r.body.append('fillcolor="#F5F5F5"')
            with r.subgraph(name='cluster_pt_raw_inr') as rinr:
                rinr.body.append('label="In-Network Files"')
                rinr.body.append('style="filled"')
                rinr.body.append('color="#808080"')
                rinr.body.append('fillcolor="#DCDCDC"')
                rinr.node('meta_inr', 'meta_inr', fillcolor='#F5F5F5', style='filled', shape='tab')
                rinr.node('in_network_file', '.../schema=inr/*.json.gz', fillcolor='#FFFACD', style='filled',
                          shape='folder')
            with r.subgraph(name='cluster_pt_raw_prg') as rprg:
                rprg.body.append('label="Provider Reference Files"')
                rprg.body.append('style="filled"')
                rprg.body.append('color="#808080"')
                rprg.body.append('fillcolor="#DCDCDC"')
                rprg.node('meta_prg', 'meta_prg', fillcolor='#F5F5F5', style='filled', shape='tab')
                rprg.node('provider_reference_file', '.../schema=prg/*.json.gz', fillcolor='#FFFACD', style='filled',
                          shape='folder')
        with c.subgraph(name='cluster_pt_stage') as s:
            s.body.append('label="pt_stage"')
            s.body.append('style="filled"')
            s.body.append('color="#808080"')
            s.body.append('fillcolor="#F5F5F5"')
            s.node('inr', '', fillcolor='#CAD9EF', style='filled', **tbl_link('pt_stage', 'inr'), shape='point')
            s.node('prg', '', fillcolor='#CAD9EF', style='filled', **tbl_link('pt_stage', 'prg'), shape='point')
            s.node('v_inr_header', 'inr_header', fillcolor='#CAD9EF', style='filled')
            s.node('v_inr_network', 'inr_network', fillcolor='#CAD9EF', style='filled')
            s.node('v_inr_provider', 'inr_provider', fillcolor='#CAD9EF', style='filled')
            s.node('v_prg_pg', 'prg_pg', fillcolor='#CAD9EF', style='filled')
            s.node('in_coverage', 'in_coverage', fillcolor='#CAD9EF', style='filled',
                   **tbl_link('pt_stage', 'in_coverage'))
            s.node('in_rate', 'in_rate', fillcolor='#CAD9EF', style='filled', **tbl_link('pt_stage', 'in_rate'))
            s.node('in_provider', 'in_provider', fillcolor='#CAD9EF', style='filled',
                   **tbl_link('pt_stage', 'in_provider'))
        with c.subgraph(name='cluster_pt') as p:
            p.body.append('label="pt"')
            p.body.append('style="filled"')
            p.body.append('color="#808080"')
            p.body.append('fillcolor="#F5F5F5"')
            p.node('v_in_coverage', 'in_coverage', fillcolor='#CAD9EF', style='filled,dashed',
                   **tbl_link('pt', 'in_coverage'))
            p.node('v_in_rate', 'in_rate', fillcolor='#CAD9EF', style='filled,dashed', **tbl_link('pt', 'in_rate'))
            p.node('v_in_provider', 'in_provider', fillcolor='#CAD9EF', style='filled,dashed',
                   **tbl_link('pt', 'in_provider'))

        dot.edge('in_network_file', 'inr', ltail='cluster_pt_raw_inr')
        dot.edge('provider_reference_file', 'prg', ltail='cluster_pt_raw_prg')

        dot.edge('inr', 'v_inr_header')
        dot.edge('inr', 'v_inr_network')
        dot.edge('inr', 'v_inr_provider')
        dot.edge('prg', 'v_prg_pg')

        dot.edge('v_inr_header', 'in_coverage')
        dot.edge('v_inr_network', 'in_coverage')
        dot.edge('v_inr_header', 'in_rate')
        dot.edge('v_inr_network', 'in_rate')
        dot.edge('v_inr_provider', 'in_rate')
        dot.edge('v_inr_network', 'in_provider')
        dot.edge('v_inr_header', 'in_provider')
        dot.edge('v_inr_provider', 'in_provider')
        dot.edge('v_prg_pg', 'in_rate')
        dot.edge('v_prg_pg', 'in_provider')

        dot.edge('in_coverage', 'v_in_coverage')
        dot.edge('in_rate', 'v_in_rate')
        dot.edge('in_provider', 'v_in_provider')

    html = dot._repr_image_svg_xml()
    html = re.sub(r'<svg width=\"\d*pt\" height=\"\d*pt\"',
                  '<div style="text-align:center;"><svg width="900pt" aligned=center', html)
    html = re.sub(r'font-size=\"14.00\">Fact Tables</text>', 'font-size=\"12.00\">Fact Tables</text>', html)
    html = re.sub(r'font-size=\"14.00\">Dimension Tables</text>', 'font-size=\"12.00\">Dimension Tables</text>', html)
    html = re.sub(r'font-size=\"14.00\">Reference Tables</text>', 'font-size=\"12.00\">Reference Tables</text>', html)
    html = re.sub(r'font-size=\"14.00\">DI Operational Tables</text>',
                  'font-size=\"12.00\">DI Operational Tables</text>', html)
    html = re.sub(r'stroke-width=\"2\"', 'stroke-width=\"4\"', html)
    html = re.sub(r'</svg>', '</div</svg>', html)

    return html