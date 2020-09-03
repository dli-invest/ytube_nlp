from jinja2 import Template
import pandas as pd

# make str path to html url
# def path_to_url(path):
#   return f'<a href="./{path}">{path}</a>'
yt_df = pd.read_csv("yt_data.csv", index_col="video_id")
yt_df = yt_df.sort_values(by=["date"])
# yt_df['path'] = yt_df['path'].apply(lambda x: path_to_url(x)) # f'<a href="./{investing/2020-07-09/-5aG8r2fkM0.html}'
try:
    options = dict(
        HTML_TABLE=yt_df.to_html(
            table_id="datatable", classes="uk-table cell-border compact stripe"
        )
    )
    with open("lib/index.jinja2") as file_:
        template = Template(file_.read())
    index_html = template.render(**options)
    with open("test_index.html", "w") as file_:
        file_.write(index_html)
except Exception as e:
    print(e)