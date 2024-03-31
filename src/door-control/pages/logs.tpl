<html>
  <head>
	<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Source+Code+Pro">
    <link rel="stylesheet" href="/style.css">
  </head>
  <body>
    <div class="container">
      <h1>Logs</h1>
	  <div>Showing the last {{logNum}} log messages. Loglevel: <b>{{loglevel}}</b><br/>Timezone is <b>UTC</b></div>
      <table>
        <thead>
          <tr>
            <th>Logs</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="logs">{{logs}}</td>
          </tr>
        </tbody>
      </table>
      <div class="center_link"><a href="/">&#8962;</a></div>
    </div>
  <body>
</html>
