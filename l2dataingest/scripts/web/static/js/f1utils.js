var ang = 0;
var mapx = 540;
var mapy = 270;

var track = {
  x: 0,
  y: 0,
  name: "Track",
  line: {
    color: 'white',
    width: 8
  }
}

car = {
  x: [0,0],
  y: [0,0],
  mode: 'markers',
  name: "Car",
  marker: {
    size: 14,
    color: 'red',
    symbol: "circle-dot"
  }
}

var data = [track, car];

var layout = {
   
    showlegend: false,
    hovermode: 'closest',
    xaxis: {
        zeroline: false,
        showgrid: false,
        showline: false,
        showticklabels: false,
        titlefont: {
          font: {
            color: 'rgb(204, 204, 204)'
          }
        },
        tickfont: {
          font: {
            color: 'rgb(102, 102, 102)'
          }
        }
    },
    yaxis: {
        zeroline: false,
        showgrid: false,
        showline: false,
        showticklabels: false,
        titlefont: {
          font: {
            color: 'rgb(204, 204, 204)'
          }
        },
        tickfont: {
          font: {
            color: 'rgb(102, 102, 102)'
          }
        }
    },
    margin: {
        l: 5,
        r: 10,
        b: 5,
        t: 5
    },
    legend: {
        font: {
          size: 12,
        },
        yanchor: 'bottom',
        xanchor: 'right'
    },
    side: 'bottom',
    width: mapx,
    height: mapy,
    paper_bgcolor:'rgb(100,100,100,0.1)',
    plot_bgcolor:'rgb(10, 140, 0)'
  };


function rot(x1,y1) {
    var cx = 0;
    var cy = 0;
  
    var radians = (Math.PI / 180) * ang,
    cos = Math.cos(radians),
    sin = Math.sin(radians),
    nx = (cos * (x1 - cx)) + (sin * (y1 - cy)) + cx,
    ny = (cos * (y1 - cy)) - (sin * (x1 - cx)) + cy;
    return [nx, ny];
}

function convertTime(laptime) {
  laptime = laptime / 1000; // Sent in milliseconds
  var lap = "";  // Full Lap time format
  var slap= "";  // Short Lap time format
  var clap= "";  // Current Lap format
 
  msecs = (laptime + "").split(".")[1];
  if (msecs == null) msecs = "000";

  // Hours, minutes and seconds
  var hrs = ~~(laptime / 3600);
  var mins = ~~((laptime % 3600) / 60);
  var secs = ~~laptime % 60;

  // Output like "1:01" or "4:03:59" or "123:03:59"
  if (hrs > 0) {
      lap += "" + hrs + ":" + (mins < 10 ? "0" : "");
  }

  if (mins > 0 ) {
    lap += "" + mins + ":" + (secs < 10 ? "0" : "");
  }
  
  msecStr = msecs.toString();
  
  // Pad out zeros
  if (msecStr.length == 1) {
    msecStr += "" + "00";
  } else if (msecStr.length == 2) {
    msecStr += "" + "0";
  }
 
  clap = lap + "" + secs + "." + msecStr.substring(0,1);
  lap += "" + secs + "." + msecStr;
  slap += "" + secs + "." + msecStr;

  return {'lap': lap, 'shortlap': slap, 'current': clap};
}
