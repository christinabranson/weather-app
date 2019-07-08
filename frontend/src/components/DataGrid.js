import React from "react";

class DataGrid extends React.Component {
  render() {
    console.log("DataGrid.render");
    console.log(this.props.data);
    var data = this.props.data.data;
    return (
      <div class="container">
        <div class="row">
        {data.map(item => (
          <div key={item.label} class="col px-1">
              <small>{item.label}</small>
              <div class="databox">
                <div class="fill empty" style={{height:item.percent_empty}}></div>
                <div class="fill accumulation" style={{height:item.percent_accumulation}}></div>
                <div class="fill manual" style={{height:item.percent_manual}}></div>
                <div class="fill rain" style={{height:item.percent_rain}}></div>
              </div>
          </div>
        ))}
        </div>
      </div>
    );
  }
}
export default DataGrid;