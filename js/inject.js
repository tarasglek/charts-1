/*
open /Applications/Google\ Chrome.app --args --allow-running-insecure-content
npm install http-server -g

openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out cert.pem
http-server -S -P http://localhost:4200
 (function() {
    var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
    po.src = "https://127.0.0.1:8081/inject.js";
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
  })();
*/
(function addButton() {
  var navbar = document.getElementsByClassName("pure-nav")[0];
  var li = document.createElement('li');
  li.innerHTML = "<a href=/k8s><em class=\"headline-font\">CONTAINERS</em></a>";
  li.className = "selected";
  Array.from(navbar.children).forEach(function(element) {
    element.className = null;
  }, this);
  navbar.appendChild(li);
  var content = document.getElementsByClassName("pure-content")[0];
  content.style.backgroundColor='white';
  content.innerHTML = `<iframe style=\" width: 100%; height: ${content.clientHeight}px ;display: block; top: 0; left: 0;\" src=\"https://127.0.0.1:8081/charts\"></iframe>`;
})()
