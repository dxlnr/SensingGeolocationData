let table;
let jlm_table;
let canvaswidth = 600;
let rLat = [];
let rLong = [];
let pLat = [];
let pLong = [];


function preload() {
  //my table is comma separated value "csv"
  //and has a header specifying the columns labels
  //table = loadTable('JLM.csv', 'csv', 'header');
  jlm_table = loadTable('jlm_datapoints.csv', 'csv', 'header');
  //the file can be remote
  //table = loadTable("http://p5js.org/reference/assets/mammals.csv",
  //                  "csv", "header");
}

function convertValues(tableobj) {
  /**
    Convert the ranges of the Latitude and Longitude on the ranges of the canvas.
    Enable full use of the canvas.
    */
  let raLat = [];
  let raLong = [];
  let offparam = 25;
  lat = float(tableobj.getColumn('Latitude'));
  long = float(tableobj.getColumn('Longitude'));

  maxLat = max(lat);
  maxLong = max(long);
  minLat = min(lat);
  minLong = min(long);

  for (let i = 0; i < tableobj.getRowCount(); i++){
    const tmpLat = float(lat[i]);
    const tmpLong = float(long[i]);
    raLat[i] = map(tmpLat, minLat, maxLat, offparam, canvaswidth - offparam);
    raLong[i] = map(tmpLong, minLong, maxLong, offparam, canvaswidth - offparam);
  }

  return [raLat, raLong];
}

function setup() {
  createCanvas(canvaswidth, canvaswidth);
  background(200);

  let r = convertValues(table);
  rLat = r[0];
  rLong = r[1];

  let pa = convertValues(jlm_table);
  pLat = pa[0];
  pLong = pa[1];

  /*
  for (let i = 0; i < table.getRowCount(); i++){
    const numbers = int(table.getString(i, 'times'));
    const size = map(numbers, 0, 59875, 0, 1600);
    const fillColor = map(numbers, 0, 59875, 0, 255);
    let x_axis = rLat[i];
    let y_axis = rLong[i];
    circle(x_axis, y_axis, size);
    fill(fillColor);
  }

  for (let k = 0; k < jlm_table.getRowCount(); k++){
    let x_p = pLat[k];
    let y_p = pLong[k];
    point(x_p, y_p);
    strokeWeight(20);
  }
  */

  for (let k = 0; k < jlm_table.getRowCount(); k += 1){

    if ((k+3) == jlm_table.getRowCount()){
      break;
    }

    let x_p1 = pLat[k];
    let y_p1 = pLong[k];

    let x_p2 = pLat[k+3];
    let y_p2 = pLong[k+3];

    let x_control_p1 = pLat[k+1];
    let y_control_p1 = pLong[k+1];

    let x_control_p2 = pLat[k+2];
    let y_control_p2 = pLong[k+2];

    //let x_control_p1 = x_p1 + random(20);
    //let y_control_p1 = y_p1 + random(20);

    //let x_control_p2 = x_p2 + random(20);
    //let y_control_p2 = y_p2 + random(20);

    noFill();
    //bezier(x_p1, y_p1, x_control_p1, y_control_p1, x_control_p2, y_control_p2, x_p2, y_p2);
    curve(x_p1, y_p1, x_control_p1, y_control_p1, x_control_p2, y_control_p2, x_p2, y_p2);
    strokeWeight(2);
  }

}

function draw(){
  //rect(10,20,30,40);

}
