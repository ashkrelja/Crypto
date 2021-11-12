        (() => {
        const update = () => {
          fetch('/reddit_line_data')
            .then(resp => resp.json())
            .then(data =>Plotly.react('data-container', data, {}));
          fetch('/reddit_pie_data')
            .then(resp => resp.json())
            .then(data => Plotly.react('pie-container', data, {}));
         fetch('/reddit_total')
            .then(resp => resp.json())
            .then(html => {document.getElementById('earnings').innerHTML = html;});
        };
        update();
        setInterval(update, 2000);
      })();

   $("#data-container").css({
    "width": "98%",
    "height": "100%"
    });


