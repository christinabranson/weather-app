import React from "react";

class DataTable extends React.Component {
  render() {
    console.log("DataTable.render");
    console.log(this.props);

        return (
            <table className="table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Rain Amount</th>
                        <th>Accumulation</th>
                    </tr>
                </thead>
                <tbody>
                    {this.props.data.data.map(item => (
                      <tr key={item.label}>
                        <td>{item.label}</td>
                        <td>{item.amount_rain}</td>
                        <td>{item.amount_accumulation}</td>
                      </tr>
                    ))}
                </tbody>
            </table>
        );
  }
}
export default DataTable;