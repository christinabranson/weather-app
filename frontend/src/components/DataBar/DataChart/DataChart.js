import React from "react";
import ReactDOM from "react-dom";
import { Chart } from 'react-chartjs-2';

class DataChart extends React.Component {

  chart = null;

  componentDidMount() {
    this.configureChart();
  }

  extractLabelFromData(jsonData) {
    var labelArray = [];
    for (var jsonDataI = 0; jsonDataI < jsonData.data.length; jsonDataI++) {
      var jsonDataPiece = jsonData.data[jsonDataI];
      labelArray.push(jsonDataPiece.label);
    }

    return labelArray;
  }

  extractDataAmountFromData(jsonData) {
    var dataArray = [];
    for (var jsonDataI = 0; jsonDataI < jsonData.data.length; jsonDataI++) {
      var jsonDataPiece = jsonData.data[jsonDataI];
      dataArray.push(jsonDataPiece.amount_rain);
    }

    return dataArray;
  }

  extractDataAccumulationFromData(jsonData) {
    var dataArray = [];
    for (var jsonDataI = 0; jsonDataI < jsonData.data.length; jsonDataI++) {
      var jsonDataPiece = jsonData.data[jsonDataI];
      dataArray.push(jsonDataPiece.amount_accumulation);
    }

    return dataArray;
  }

  configureChart = () => {
    const chartCanvas = ReactDOM.findDOMNode(this.chart);

    var jsonData = this.props.data;
    console.log(jsonData.data);

    var labelsArray = this.extractLabelFromData(jsonData);
    var dataAmountArray = this.extractDataAmountFromData(jsonData);
    var dataAccumulationArray = this.extractDataAccumulationFromData(jsonData);

    console.log(dataAmountArray);
    console.log(dataAccumulationArray);

    const mixedChart = new Chart(chartCanvas, {
      type: "bar",
      data: {
        datasets: [
                    {
            label: "Daily Amount",
            data: dataAmountArray,
            type: "bar",
            backgroundColor: "#007bff"
          },
          {
            label: "Weekly Accumulation",
            data: dataAccumulationArray,
            type: "bar",
            backgroundColor: "#6c757d"
          }
        ],
        labels: labelsArray
      },
      options: {
        elements: {
          line: {
            tension: 0.000001
          }
        },
        tooltips: {
          displayColors: false
        },
        legend: {
          display: true
        },
        scales: {
          yAxes: [
            {
              display: true,
              // stacked: true,
              ticks: {
                beginAtZero: true
              }
            }
          ],
          xAxes: [
            {
              display: true,
              stacked: true,
              barThickness: 25,
              ticks: {
                beginAtZero: true
              }
            }
          ]
        }
      }
    });
  };

   render() {
        console.log("DataChart.render");
    console.log(this.props);
    return (
      <div>
        <canvas
          ref={chart => {
            this.chart = chart;
          }}
        />
      </div>
    );
  }
}
export default DataChart;