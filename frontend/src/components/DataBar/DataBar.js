import React from "react";
import DataTable from "./DataTable/DataTable";
import DataChart from "./DataChart/DataChart";

class DataBar extends React.Component {
  render() {
    console.log("DataBar.render");
    console.log(this.props);

        return (
            <div className="row">
               <div className="col-lg-6 col-xs-6">
                  <div className="box box-primary">
                     <div className="box-header with-border">
                        <h3 className="box-title">The Data</h3>
                     </div>
                     <div className="box-body">
                        <DataTable data={this.props.data} />
                     </div>
                  </div>
               </div>
               <div className="col-lg-6 col-xs-6">
                  <div className="box box-primary">
                     <div className="box-header with-border">
                        <h3 className="box-title">The Data, Visualized</h3>
                     </div>
                     <div className="box-body">
                        <DataChart data={this.props.data} />
                    </div>
                  </div>
               </div>
            </div>
        );
  }
}
export default DataBar;