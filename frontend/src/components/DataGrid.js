import React from "react";
import { Tooltip } from 'reactstrap';
import DataBox from "./DataBox";

class DataGrid extends React.Component {
  render() {
    console.log("DataGrid.render");
    console.log(this.props.data);
    var data = this.props.data ? this.props.data.data : null;
    if (data){
        return (
          <div className="container">
            <div className="row">
            {data.map(item => (
              <div key={item.label} class="col px-1">
                  <p>{item.day}</p>
                  <small>{item.date}</small>
                  <DataBox item={item} />
              </div>
            ))}
            </div>
          </div>
        );
    } else {
        return null;
    }
  }
}
export default DataGrid;