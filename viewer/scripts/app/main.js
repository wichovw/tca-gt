define(['./tca', './graph'], function (tca, graph) {
  
  tca.start();
  
  
  document.body.appendChild(graph.view);
  graph.animate();

});