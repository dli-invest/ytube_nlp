import pandas as pd
from jinja2 import Template

yt_df = pd.read_csv("yt_data.csv")
options = dict(
    HTML_TABLE=yt_df.to_html(
        table_id="datatable",
        classes="uk-table cell-border compact stripe",
        render_links=True,
    )
)
with open("lib/index.jinja2") as file_:
    template = Template(file_.read())
index_html = template.render(**options)
with open("scripts/index_gen_test.html", "w") as file_:
    file_.write(index_html)