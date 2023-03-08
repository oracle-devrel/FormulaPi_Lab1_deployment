/////////////////////////////
// Connect to RabbitMQ
// Track Map is defined by first record hitting MQ 
// New Session Detected, triggers new map
// calls newSession API (Returns, Track, Version & Fastest Lap Time)
// Call reflap wih Track and Version to get Reference for that Specific Track
// 
// Uses referenceLap function to return track map
//
/////////////////////////////



// Create a client instance
const clientID = "livelapsMQ" + parseInt(Math.random() * 100);
var wsbroker = location.hostname;  // mqtt websocket enabled broker
var wsport = 15675; // port for above

client = new Paho.MQTT.Client(wsbroker, wsport, '/ws', clientID);
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

var keepS1 = 0;
var keepS2 = 0;
var f_s1 = 0;
var f_s2 = 0;
var f_lt = 0;
var bestLap = 0;
var c_session = "";
var xl = [];
var yl = [];
var col = [];
var turndata=[];
var inlap =0;

var apiurl = "https://yj6gtaivgb4zvoj-fortatp.adb.ap-sydney-1.oraclecloudapps.com/ords/anziot/f1/";

console.log("Gentlemen.. start your engines");

var options = {
  timeout: 3,
  keepAliveInterval: 30,
  userName: rmqusername,
  password: rmqpassword,
  onSuccess: onConnect,  
  onFailure: onFailure,
};

function onConnect() {
  console.log("RMQ Connect");
  document.getElementById("message").innerHTML = "Connected to F1Sim";
  client.subscribe('', {qos: 1});
}

function onFailure(message) {
  console.log("RMQ Failed: ", message);
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("RMQ Connection Lost: "+responseObject.errorMessage);
  }
};

// Console Switch to turn Data Connector (to MQ) on and off
function consoleSwitch() {
  // Get the checkbox
  var checkBox = document.getElementById("sw_console");
  // Get the output text
  var text = document.getElementById("message");

  // If the checkbox is checked, display the output text
  if (checkBox.checked == true){
    
    // connect to RabbitMQ 
    message.innerHTML = "Connecting to F1Sim";
    console.log("Connect to ", wsbroker);
    // connect the client
    client.connect(options);

    document.getElementById("s1_acc").style.width = "0%";
    document.getElementById("s1_br").style.width = "0%";

  } else {
  // Disconnect RabbitMQ
    client.disconnect();
    message.innerHTML = "Disconnected";
    document.getElementById("info").innerHTML = 'BOX BOX';
    document.getElementById("info_data").innerHTML = '&nbsp;';
  }
}

// Called when a message arrives from MQ
function onMessageArrived(message) {

  //payload = message.payloadString.replace(/'/g, '"').replace(/^"(.+(?="$))"$/, '$1');
  document.getElementById("message").innerHTML = "Receiving Data";

  // extract SESSION ID as a string from payload
  payload =  message.payloadString.replace(/"m_session": (\d*),/, '"m_session": "$1",');
  const telemetry = JSON.parse(payload);
  //console.log(telemetry);

  // Fetch Session data if never seen session before
  if (typeof telemetry.m_session !== 'undefined' && c_session !== telemetry.m_session) fetchSession(telemetry.m_session);

  if (typeof telemetry.m_speed !== 'undefined' ) {
    // TELEMETRY DATA Packet
    speedkm = telemetry.m_speed;
    acc_pc = (telemetry.m_throttle *100);
    brk_pc = (telemetry.m_brake * 100);

    if (telemetry.m_gear == 0 ) {
      gear = "N";
    } else if (telemetry.m_gear <0 ) {
      gear = "R";
    } else {
      gear = telemetry.m_gear.toFixed(0);
    }
    
    document.getElementById("s1_acc").style.width = acc_pc + "%";
    document.getElementById("s1_br").style.width = brk_pc + "%";

    document.getElementById("s1_speed").innerHTML = speedkm.toFixed(0);
    document.getElementById("s1_rpm").innerHTML = telemetry.m_engineRPM.toFixed(0);
    document.getElementById("s1_gear").innerHTML = gear;
  }

  if (typeof telemetry.m_current_lap_num !=='undefined') {
    // LAP DATA Packet
    //console.log(telemetry);

    // If lap is 0, then technically sitting in pits
    if (telemetry.m_lap_distance >0 ) {
      inlap = 1;
      document.getElementById("s1_lap").innerHTML = telemetry.m_current_lap_num;
    } else {
      inlap = 0;
      document.getElementById("s1_lap").innerHTML = 'PIT';
      document.getElementById("s1_sec").innerHTML = '-';
    }

    if (telemetry.m_sector == 0 && telemetry.m_current_lap_num > 1) {
      // Keep Sector Times for last lap on until first sector is complete
      s3time = telemetry.m_last_lap_time_in_ms - keepS1 - keepS2;

      document.getElementById("s1_s1").innerHTML = convertTime(keepS1).shortlap;
      document.getElementById("s1_s2").innerHTML = convertTime(keepS2).shortlap;
      document.getElementById("s1_s3").innerHTML = convertTime(s3time).shortlap;
      document.getElementById("s1_s1").style.color = "var(--f1-timing-green)";
      document.getElementById("s1_s2").style.color = "var(--f1-timing-green)";
      document.getElementById("s1_s3").style.color = "var(--f1-timing-green)";
    } else {
      document.getElementById("s1_s1").innerHTML = convertTime(telemetry.m_sector1_time_in_ms).shortlap;
      document.getElementById("s1_s2").innerHTML = convertTime(telemetry.m_sector2_time_in_ms).shortlap;
      document.getElementById("s1_s3").innerHTML = convertTime(0).shortlap;
      document.getElementById("s1_s1").style.color = "var(--f1-timing-yellow)";
      document.getElementById("s1_s2").style.color = "var(--f1-timing-yellow)";
      document.getElementById("s1_s3").style.color = "var(--f1-timing-yellow)";
      keepS1 = telemetry.m_sector1_time_in_ms;
      keepS2 = telemetry.m_sector2_time_in_ms;
    }
   
    if (bestLap == 0 || (bestLap > 0 && telemetry.m_last_lap_time_in_ms != 0 && telemetry.m_last_lap_time_in_ms < bestLap)) 
    {
      bestLap = telemetry.m_last_lap_time_in_ms;
      document.getElementById("s1_blap").innerHTML = convertTime(bestLap).lap;
      document.getElementById("s1_blap").style.color = "var(--f1-timing-green)";
    }

    document.getElementById("s1_sec").innerHTML = telemetry.m_sector+1;
    document.getElementById("s1_clap").innerHTML = convertTime(telemetry.m_current_lap_time_in_ms).lap;
    document.getElementById("s1_llap").innerHTML = convertTime(telemetry.m_last_lap_time_in_ms).lap;
  }

  if (typeof telemetry.m_worldPosX !== 'undefined') {
    // MOTION DATA Packet
    var car_posx=[];
    var car_posy=[];
    // Detect Turn
    var turn = inTurn(telemetry.m_worldPosX, telemetry.m_worldPosY)
    if (inlap && turn <100) {
      document.getElementById("info").innerHTML = "Turn";
      document.getElementById("info_data").innerHTML = turn;
    } else if (inlap) {
      document.getElementById("info").innerHTML = "&nbsp;";
      document.getElementById("info_data").innerHTML = "&nbsp;";
    }
  
    // Rotate car worldX,worldY position based on Map Rotation
    car_posx.push(rot(telemetry.m_worldPosX, telemetry.m_worldPosY)[0]);
    car_posy.push(rot(telemetry.m_worldPosX, telemetry.m_worldPosY)[1]);

    data[1].x = car_posx;
    data[1].y = car_posy;
      
    Plotly.newPlot('graph1', data, layout);
  }
}

// New Session is Identified...
function fetchSession(sessionid) {
  console.log("New Session: " + sessionid);
  c_session = sessionid; // Store so we don't keep fetching API data
  document.getElementById("info_data").innerHTML =c_session;
  document.getElementById("info").innerHTML = "Session";
  var sessionapi = apiurl + "newSession/"+ c_session

  // go Get Session Details
  fetch(sessionapi)
    .then((response) => response.json())
    .then((data) => sessionData(data))
}

// Fetch Session Details (to get Track and Fastest Lap details)
function sessionData(data) {

  var sessiondata = data.SESSIONDATA;
  var lapi = apiurl + "reflap/";

  if (typeof sessiondata != "undefined" && sessiondata !=null) {
    lapi = lapi + sessiondata.M_TRACKID + "/" + sessiondata.M_PACKET_FORMAT;
    bestLap = sessiondata.TRACK_FASTEST_IN_MS;
    document.getElementById("s1_blap").innerHTML = convertTime(bestLap).lap;
  } else {
    // Default to Home Track
    lapi = lapi + hometrack + "/" + gameversion;
  }
  //console.log("Fetching Reference Lap:" + lapi)

  // Now get Lap details and Draw Cicuit
  fetch(lapi)
  .then((response) => response.json())
  .then((data) => trackmap(data))
}

// Get Track Map & Turn data
function trackmap(data) {
 
  var trackdata = data.LAPDATA;
  var mapdata = data.TRACK_DETAIL;
  turndata = data.TURNDATA;

  console.log(turndata.length + " Turns");
  //console.log(turndata);

  ang = mapdata.ROTATION;

  xl = [];
  yl = [];
  col = [];

  for(var i =0;i < trackdata.length;i++)
  {
      rotn = rot(trackdata[i].WPX, trackdata[i].WPY);

      xl.push(rotn[0]);
      yl.push(rotn[1]);

      if (trackdata[i].M_SECTOR == 1) {
        col.push('rgb(150,0,0)');
      } else if (trackdata[i].M_SECTOR == 2) {
        col.push('rgb(0,0,120');
      } else { 
        col.push('rgb(180,180,0');
      }
  }

  track.x = xl;
  track.y = yl;
  //track.line.color = col

  //layout.width = mapdata.MAP_WIDTH;;
  //layout.height = mapdata.MAP_HEIGHT;

  var car_posx=[];
  var car_posy=[];

  car_posx.push(270);
  car_posy.push(-406);
  
  // Use World PosX to draw car position
  car.x = car_posx
  car.y = car.posy

  // Set Map Display Size (get from API. Telemetry screen is 1x 0.5y)
  data = [track, car];
  Plotly.newPlot('graph1', data, layout,  {displayModeBar: false});

}

function inTurn(x,y) {

  var turn=999;
  console.log(x,y);

  for(var ct =0; ct < turndata.length; ct++)
  {
    if (turn == 999 && x > turndata[ct].CX1 && x < turndata[ct].CX2 && y > turndata[ct].CY1 && y < turndata[ct].CY2) {
      turn = ct;
    }
  }

  //if (turn != 999 ) console.log("In turn " + turn);
  return turn+1;
}