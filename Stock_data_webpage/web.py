from flask import Flask,render_template
app=Flask(__name__)

@app.route('/plot/')
def plot():
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.models.annotations import Title
    # from bokeh.io import show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    start = datetime.datetime(2020, 7, 23)
    end = datetime.datetime(2021, 1, 23)

    df = data.DataReader(name="TSLA", data_source="yahoo", start=start, end=end)

    def inc_dec(c, o):
        if c > o:
            value = "Increase"
        elif c < o:
            value = "Decrease"
        else:
            value = "Equal"
        return value

    df['Status'] = [inc_dec(c, o) for c, o in zip(df.Close, df.Open)]
    df["Middle"] = (df.Open + df.Close) / 2
    df["Height"] = abs(df.Close - df.Open)
    p = figure(x_axis_type='datetime', width=800, height=300, sizing_mode='scale_width')
    t = Title()
    t.text = "Tesla Candlestick Chart 7/23/2020 - 1/23/2021"
    p.title = t

    p.grid.grid_line_alpha = 0.3
    hours_12 = 12 * 60 * 60 * 1000

    p.segment(df.index, df.High, df.index, df.Low, color="black")
    p.rect(df.index[df.Status == "Increase"], df.Middle[df.Status == "Increase"], hours_12,
           df.Height[df.Status == "Increase"], fill_color="green", line_color="black")
    p.rect(df.index[df.Status == "Decrease"], df.Middle[df.Status == "Decrease"], hours_12,
           df.Height[df.Status == "Decrease"], fill_color="red", line_color="black")

    script1, div1 = components(p)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files
    return render_template("plot.html", script1=script1, div1=div1, cdn_css=cdn_css,cdn_js=cdn_js)


@app.route('/')
def layout():
    return render_template("layout.html")

@app.route('/home')

def home():
    return render_template("home.html")


@app.route('/about')

def about():
    return render_template("about.html")




if __name__ == "__main__":
    app.run(debug=True)