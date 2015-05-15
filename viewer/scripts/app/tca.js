define(['jquery', './data'], function ($, data) {
  //Stat connection and keep updating
  var start = function(){
    $.ajax(data.get('opts.host') + "/start")
    .then(function(response){
      data.set('matrix', response);
      //Start updating each 300ms
      setInterval(update, data.get('opts.interval'));
    }, function(fail){
      alert('Connection fail');
      console.log(fail);
    });
  };
  
  //Update function
  var update = function(){
    $.ajax(data.get('opts.host') + "/update")
    .then(function(response){
      data.set('matrix', response);
    }, function(fail){
      alert('Connection fail');
      console.log(fail);
      //Stop updating
      clearInterval();
    });
  };
  
  return {start: start};
});