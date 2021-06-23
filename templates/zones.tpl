<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Time Zones</title>
  <style>
  table {
    border-collapse: collapse;
  }
  thead {
    position: sticky;
    top: 0;
    border-bottom: 2px solid #000;
  }
  tr:nth-child(even) {
    background-color: #f2f2f2;
  }
  th, td {
    vertical-align: middle;
    border: 1px solid #ddd;
    padding: 8px;
  }
  th {
    background-color: #ccc;
    padding-top: 12px;
    padding-bottom: 12px;
    text-align: left;
  }
  </style>
</head>
<body>
  <table>
    <thead>
      <tr><th>Time Zone</th><th>UTC Offset</th></tr>
    </thead>
    <tbody>
      % for k, v in zones.items():
      <tr><td><a href="/{{k}}">{{k}}</a></td><td><a href="/timezones/{{v}}">{{v}}</a></td></tr>
      % end
    </tbody>
  </table>
</body>
</html>
