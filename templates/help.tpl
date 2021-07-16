<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>TimeService - Help</title>
  </head>
  <body>
    <h1>TimeService Help</h1>
    <h2>Introduction</h2>
    <p>TimeService is a simple service that gives time in UTC, or a requested time zone,
       represented as an ISO-8601 string. This service also includes the list of available
       time zones optionally filtered by the UTC offset or an area.</p>
    <h2>How to Use</h2>
    <h3>Get the time</h3>
    <p>To get the time in UTC (the default time zone) just make a request to the
      <a href="/">/ endpoint</a></p>
    <p>To get the time in a different time zone just make a request to the name
      of the time zone. For example, to get the time of New York,
      request the <a href="/America/New_York">America/New_York</a> time zone.</p>
    <h3>Get time zones</h3>
    <p>To get the list of supported time zones, make a request to the <a href="/timezones">/timezones</a>
      endpoint.<p>
      <p>The output can be controlled using the HTTP <em>Accept</em>
      header. Supported types are: </p>
      <ul>
      <li>JSON: <em>application/json</em></li>
      <li>HTML: <em>text/html</em></li>
      <li>CSV with header: <em>text/csv</em></li>
      <li>Text (default): <em>text/plain</em></li>
      </ul>
    <h4>Filtering time zones</h4>
    <p>You can filter time zones in two ways:</p>
    <h5>UTC offset</h5>
    <p> This will return all the time zones for the requested offset. </p>
    <p>To filter time zones by their UTC offset, simply add the offset for the
      time zones you want, for example, to get UTC +0500 you can use <a href="/timezones/+0500">/timezones/+0500</a>.
      Values of <a href="/timezones/+05">+05</a>, <a href="/timezones/05">05</a>, <a href="/timezones/+500">+500</a>,
      <a href="/timezones/500">500</a>, <a href="/timezones/+5">+5</a> and <a href="/timezones/5">5</a> are also
      valid and yield the same results.</p>
    <h5>Area</h5>
    <p> This will return all the time zones of the requested area. </p>
    <p>Some time zones include an area and a location. For example, in the time
      zone named "America/New_York", "America" is the area and "New York" is the
      location. If you want to know all the time zones for an area, for example
      Antarctica, you can make a request to <a href="/timezones/antarctica">/timezones/antarctica</a>.</p>
  </body>
</html>
