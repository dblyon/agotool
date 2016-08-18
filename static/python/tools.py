from subprocess import call

def get_TOC_2_markdown_file(fn_md):
    toc = ""
    counter = 1
    with open(fn_md, "r") as fh_in:
        for line in fh_in:
            if line.startswith("#"):
                line = line.strip()
                line2add = str(counter) + ". [" + line.replace("#", "").strip() + "]" + "(#" + "-".join(line.lower().replace("#", "").strip().split()) + ")\n"
                toc += line2add
                counter += 1
    return toc

def write_TOC_2_file(fn_md, fn_out=None):
    """
    import tools
    fn = r"/Users/dblyon/modules/cpr/metaprot/DataBase_Schema.md"
    tools.write_TOC_2_file(fn)
    """
    toc = get_TOC_2_markdown_file(fn_md)
    with open(fn_md, "r") as fh_in:
        lines = fh_in.readlines()
    if not fn_out:
        fn_out = fn_md
    with open(fn_out, "w") as fh_out:
        fh_out.write(toc)
        for line in lines:
            fh_out.write(line)

def cut_tag_from_html(html_text, tag="style"):
    start_index = html_text.index("<{}>".format(tag))
    stop_index = html_text.index("</{}>".format(tag)) + len("</{}>".format(tag))
    html_tag = html_text[start_index:stop_index]
    html_rest = html_text[:start_index] + html_text[stop_index:]
    return html_tag, html_rest

def update_db_schema(FN_DATABASE_SCHEMA, FN_DATABASE_SCHEMA_WITH_LINKS):
    write_TOC_2_file(FN_DATABASE_SCHEMA, FN_DATABASE_SCHEMA_WITH_LINKS)
    # shutil.copyfile(FN_DATABASE_SCHEMA, FN_DATABASE_SCHEMA_WITH_LINKS)
    # write_TOC_2_file(FN_DATABASE_SCHEMA_WITH_LINKS)
    shellcmd = "grip {} --export --title='Data Base Schema'".format(FN_DATABASE_SCHEMA_WITH_LINKS)
    call(shellcmd, shell=True)
    with open(FN_DATABASE_SCHEMA_WITH_LINKS.replace(".md", ".html"), "r") as fh:
        content = fh.read()
    style_2_prepend, content = cut_tag_from_html(content, tag="style")
    text_before = r'''{% extends "layout.html" %}
        {% block head %}
        <script type="text/javascript">$(document).ready( function() {enrichment_page();});</script>
        {% endblock head %}
        {% block content %}
        <div class="container-fluid">'''
    text_after = r'''</div>
                    {% endblock content %}'''
    with open(FN_DATABASE_SCHEMA_WITH_LINKS.replace(".md", ".html"), "w") as fh:
        fh.write(style_2_prepend + "\n")
        fh.write(text_before)
        fh.write(content)
        fh.write(text_after)
