<html>
  <head>
    <link rel="stylesheet" href="/style.css">
  </head>
  <body>
    <div class="container">
      <h1>Status</h1>
      <table>
        <thead>
          <tr>
            <th>Feature</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>WiFi</td>
            <td>{{wifi_status}}</td>
          </tr>
          <tr>
            <td>MQTT Broker</td>
            <td>{{mqtt_status}}</td>
          </tr>
		  <tr>
            <td>Door closure state</td>
            <td>{{door_closed}}</td>
          </tr>
        </tbody>
      </table>
      <div class="center_link"><a href="/">&#8962;</a></div>
    </div>
  <body>
</html>
