define(['./tca', './graph', 'jquery'], function (tca, graph, $) {
  
  tca.start();
  
  $('#step').on('click', function(){
    tca.stop();
    tca.update();
  });
  
  document.body.appendChild(graph.view);
  graph.animate();

});