define(['pixi', './data'], function (PIXI, data) {
  var container = new PIXI.Container(),
  matrix = data.get('matrix'),
  size = 10,
  renderer = PIXI.autoDetectRenderer(data.get('opts.swidth'), data.get('opts.sheight'), {backgroundColor: data.get('colors.wall')}),
  refreshMatrix = function(graphics) {
    graphics.clear();
    var color = 0x000000;
    for (var i = 0; i < matrix.length; i++){
      for(var j = 0; j < matrix[0].length; j++){
        //Paint color according to type
        switch(matrix[j][i]){
          case -2: color = data.get('colors.wall'); break;
          case -1: color = data.get('colors.empty'); break;
//          default: color = data.get('colors.car'); break;
          default: color = parseInt(matrix[i][j], 16); break;


        }
        graphics.beginFill(color, 1);
        graphics.drawRect(size*i, size*j, size, size);
        graphics.endFill();
      }
    }
  },
  graphics = new PIXI.Graphics();
  //Add graphics to container
  container.addChild(graphics);

  var animate = function() {
      matrix = data.get('matrix');
      requestAnimationFrame(animate);
      refreshMatrix(graphics);
      renderer.render(container);
  }
  return {view: renderer.view, animate: animate};
});