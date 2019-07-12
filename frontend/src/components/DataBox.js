import React from "react";

class DataBox extends React.Component {
  render() {
    console.log("DataBox.render");
    console.log(this.props.item);
    var item = this.props.item;
    if (item){
        return (
            <div className={"col big-data-box "+item.today_class}>
                <span className="data-box-day">{item.day}</span><br/>
                <span className="data-box-date">{item.date}</span>
                  <div class="databox">
                    <div className="fill empty" style={{height:item.percent_empty}}></div>
                    <div className="fill accumulation" style={{height:item.percent_accumulation}}></div>
                    <div className="fill manual" style={{height:item.percent_manual}}></div>
                    <div className="fill rain" style={{height:item.percent_rain}}></div>
                  </div>
                  <table class='table'>
                    <tbody>
                      <tr>
                          <td>Rain</td>
                          <td>{item.amount_rain}in</td>
                      </tr>
                      <tr>
                          <td>Manual</td>
                          <td>{item.amount_manual}in</td>
                      </tr>
                      <tr>
                          <td>Accum.</td>
                          <td>{item.amount_accumulation}in</td>
                      </tr>
                      </tbody>
                  </table>
             </div>
        );
    } else {
        return null;
    }
  }
}
export default DataBox;