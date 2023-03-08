/////////////////////////////
// Use Home Track from YAML Config
// Get Reference Laps (sessionid's) using /reflap API
// 
// Use L R C Session ids to call trackmap to return 3 Map Layouts, one for Left, Right & Centre
//
/////////////////////////////

var xmlhttp = new XMLHttpRequest();

var apiurl = "https://yj6gtaivgb4zvoj-fortatp.adb.ap-sydney-1.oraclecloudapps.com/ords/anziot/f1";
var lapapi = "/mapLap/";
var lapref = "/reflap";
var trackMap = "/trackMap/"; // Send as centre / left / right
var flagapi = "https://countryflagsapi.com/png/";

// go Get Reference Sessions
fetch(apiurl + lapref)
  .then((response) => response.json())
  .then((data) => getMapData(data))

function getMapData(ref_sessions) {
  var t_api = apiurl + trackMap + ref_sessions[gameversion][hometrack]["centre"] + "/" + ref_sessions[gameversion][hometrack]["left"] + "/" + ref_sessions[gameversion][hometrack]["right"];
  xmlhttp.open("GET", t_api , true);

  xmlhttp.send();
}

xmlhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    var turns = true;

    var data = JSON.parse(this.responseText);

    var country = data.TRACK_DETAIL.COUNTRY.toLowerCase();
    if (country == "uk") country = "gb"; // Correction for Silverstone

    var flagRef = "<img src='" + flagapi + country + "' width='120px'>";

    var c_lapdata = data.CENTRE;
    var l_lapdata = data.LEFT;
    var r_lapdata = data.RIGHT;
    var turndata = data.TURNDATA;
    var GAMEHOST = data.TRACK_DETAIL.TRACK;
    ang = data.TRACK_DETAIL.ROTATION;
    mapx = data.TRACK_DETAIL.MAP_WIDTH;
    mapy = data.TRACK_DETAIL.MAP_HEIGHT;

    // Set Web components
    document.getElementById("track_id").innerHTML = data.TRACK_DETAIL.TRACK;      
    document.getElementById("track_len").innerHTML = (data.TRACK_DETAIL.TRACK_LENGTH/1000) + "km";
    document.getElementById("track_co").innerHTML = data.TRACK_DETAIL.COUNTRY;
    document.getElementById("flag").insertAdjacentHTML("afterbegin", flagRef);
    document.getElementById("track_f1lr").style.visibility = "hidden";
    document.getElementById("track_llr").style.visibility = "hidden";

    var xc = [];
    var yc = [];
    var xl = [];
    var yl = [];
    var xr = [];
    var yr = [];
    var apx = [];
    var apy = [];
    var cnx1 = [];
    var cny1 = []; 
    var cnx2 = [];
    var cny2 = []; 
    var corners =[];
    var plx =[];
    var ply =[];
    var turn = [];
    var col = [];
    var sct = [];

    //document.getElementById("graphtitle").innerHTML = "LiveLaps at " + lapdata[0].M_GAMEHOST ;

    // loop through response data set and add the x, y co-ords into the arrays - CENTRE of Track
    for(var i =0;i < c_lapdata.length;i++) {
        rotn = rot(c_lapdata[i].WPX, c_lapdata[i].WPY);
        
        xc.push(rotn[0]);
        yc.push(rotn[1]);
        
        if (c_lapdata[i].M_SECTOR == 1) {
          col.push('rgb(150,0,0)');
          sct.push('Sector 1');
        } else if (c_lapdata[i].M_SECTOR == 2) {
          col.push('rgb(0,0,120');
          sct.push('Sector 2');
        } else { 
          col.push('rgb(180,180,0');
          sct.push('Sector 3');
        }
     }
    // loop through response data set and add the x, y co-ords into the arrays - LEFT of Track
    for(var i =0;i < l_lapdata.length;i++) {
      rotn = rot(l_lapdata[i].WPX, l_lapdata[i].WPY);
      
      xl.push(rotn[0]);
      yl.push(rotn[1]);
      
    }

    for(var i =0;i < r_lapdata.length;i++) {
      rotn = rot(r_lapdata[i].WPX, r_lapdata[i].WPY);
      
      xr.push(rotn[0]);
      yr.push(rotn[1]);
      
    }

    // Turn Data
    if (turns && turndata !== null) {
  
      for(var i =0;i < turndata.length;i++) {
          rotn = rot(turndata[i].APEX_X1, turndata[i].APEX_Y1)
          apx.push(rotn[0]);
          apy.push(rotn[1]);
          // Comment in to display corner frames
          rotn = rot(turndata[i].CX1, turndata[i].CY1)
          cnx1.push(rotn[0]);
          cny1.push(rotn[1]);
          rotn = rot(turndata[i].CX2, turndata[i].CY2)
          cnx2.push(rotn[0]);
          cny2.push(rotn[1]);

          // Frame a corner
          var plx = [cnx1[i], cnx1[i], cnx2[i], cnx2[i], cnx1[i]];
          var ply = [cny1[i], cny2[i], cny2[i], cny1[i], cny1[i]];
          
          var corner = {
            x: plx,
            y: ply,
            name: "Turn " + (i+1)
          };

          corners.push(corner);

          turn.push(turndata[i].TURN);
        }
      }

    var turnFrame = 0;

    var cornerFrame = {
      x: corners[turnFrame].x,
      y: corners[turnFrame].y,
      name: corners[turnFrame].name
    }
    
    var graphDataL = {
        x: xl,
        y: yl,
        type: 'scatter',
        mode: 'lines+markers',
        marker: {
          color: 'white',
          size: 2
        },
        line: {
          color: 'grey',
          width: 18
        },
        hoverinfo: ''
      }

      var graphDataR = {
        x: xr,
        y: yr,
        type: 'scatter',
        mode: 'lines+markers',
        marker: {
          color: 'white',
          size: 2
        },
        line: {
          color: 'grey',
          width: 18
        },
        hoverinfo: ''
      }

    var turnsLabel = {
        x: apx,
        y: apy,
        type: 'scatter',
        mode: 'markers+text',
        text: turn,
        textfont:{
          'family': "formula1display", 
          'size': 10.5, 
          'color': 'white'
        },
        name: "Turn",
        marker: {
          size: 18,
          color: 'black',
          symbol: "circle"
        },
        hoverinfo: ''
      }

    var graphData3 = {
        x: xc,
        y: yc,
        type: 'scatter',
        mode: 'lines+markers',
        marker: {
          color: col,
          size: 4
        },
        line: {
          color: 'black',
          width: 6
        },
        hoverinfo: ''
      }

    var layout = {
        title: { 
          font: {
            color: 'white'
          }, 
          text: 'Circuit Layout'
        },
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
            l: 10,
            r: 10,
            b: 30,
            t: 50
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
        paper_bgcolor:'rgb(200,200,200,0.1)',
        plot_bgcolor:'rgb(10, 140, 0)'
      };

    // insert corners in here if required
    var data = [graphDataL, graphDataR, graphData3, turnsLabel];

    Plotly.newPlot('graph1', data, layout,  {displayModeBar: false});
  }
};