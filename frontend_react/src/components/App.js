import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import './main.scss';

/**
    API Endpoint: api/kitchensink
    File Endpoint: static/frontend/data.json
*/

const App = () => (
  <DataProvider endpoint="api/kitchensink" />
);

const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<App />, wrapper) : null;