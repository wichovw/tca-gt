define(['./tca', './graph', 'jquery'], function (tca, graph, $) {
  
  tca.start();
  updates = null;
  
  $('#step').on('click', function(){
    tca.stop();
    tca.update();
  });
  
  $('#start').on('click', function(){
    updates = setInterval(tca.update, 300);
  });
  
  $('#stop').on('click', function(){
    clearInterval(updates)
  });
  
  document.body.appendChild(graph.view);
  graph.animate();

});