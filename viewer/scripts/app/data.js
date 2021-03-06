define(['./opts'], function (opts) {
  var data = {
    matrix:  [
      [1, 1, 1, 1],
      [2, 2, 2, 2]
    ],
    colors: {
      wall : 0x333333,
      empty : 0xffffff,
      car: 0xa1be27 
    },
    opts: opts
  };
  
  //Use a resolver to have a better control of the data we send
  function get(param) {
    var s = param,
    o = data;
    
    s = s.replace(/\[(\w+)\]/g, '.$1'); // convert indexes to properties
    s = s.replace(/^\./, '');           // strip a leading dot
    var a = s.split('.');
    for (var i = 0, n = a.length; i < n; ++i) {
        var k = a[i];
        if (k in o) {
            o = o[k];
        } else {
            return;
        }
    }
    return o;
  }
  //Use a resolver to have a better control of the data we get
  function set(param, val) {
    var s = param,
    o = data;
    
    s = s.replace(/\[(\w+)\]/g, '.$1'); // convert indexes to properties
    s = s.replace(/^\./, '');           // strip a leading dot
    var a = s.split('.');
    for (var i = 0, n = a.length; i < n; ++i) {
        var k = a[i];
        if (k in o) {
            //If we're on the last parent, assign the value
            if(i == n - 1){
              o[k] = val;
            } else {
              //Otherwise, keep looing for o
              o = o[k];
            }
            
        } else {
            return;
        }
    }
  }
  
  function increment(param, diff) {
    this.set(param, this.get(param) + diff);
  }
  //We only expose the get, set and increment methods
  return {'get' : get, 'set' : set, 'increment' : increment};
});