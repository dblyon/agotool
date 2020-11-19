html_layout = '''
<!DOCTYPE html>
    <html>
        <head>
            <title>David's DASH</title>

        </head>
        <body class="dash-template">
            <header>
              <div class="nav-wrapper">
                <a href="/">
                    <img src="/static/images/favicon_sund.ico" class="logo" />
                    <h1>Plotly Dash Flask Tutorial</h1>
                  </a>
                <nav>
                </nav>
            </div>
            </header>
            {%app_entry%}
            <footer>
            </footer>
        </body>
    </html>
'''