import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import DataGrid from "./DataGrid";

const App = () => (
  <DataProvider source="api" endpoint="api/kitchensink" render={data => <DataGrid data={data} />} />
);
const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<App />, wrapper) : null;