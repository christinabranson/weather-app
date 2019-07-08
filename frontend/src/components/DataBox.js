import React from "react";

class DataBox extends React.Component {
  render() {
    console.log("DataBox.render");
    console.log(this.props.item);
    var item = this.props.item;
    if (item){
        return (
              <div class="data-box">
                <div className="fill empty" style={{height:item.percent_empty}}></div>
                <div className="fill accumulation" style={{height:item.percent_accumulation}}></div>
                <div className="fill manual" style={{height:item.percent_manual}}></div>
                <div className="fill rain" style={{height:item.percent_rain}}></div>
              </div>
              <div class="data-output">

              </div>
        );
    } else {
        return null;
    }
  }
}
export default DataBox;