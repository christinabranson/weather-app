import React from "react";

class HighlightBar extends React.Component {
  render() {
    console.log("HighlightBar.render");
    console.log(this.props);
    var summaryAnswer = this.props.data.summary.should_water_formatted;
    var summaryText = this.props.data.summary.should_water_message;
    var forecastData = this.props.data.summary.next_day_forecast_accumulation;
    var lastDayData = this.props.data.summary.next_day_forecast_accumulation;
    var lastWeekData = this.props.data.summary.previous_week_accumulation;

        return (
            <div className="row">
               <div className="col-lg-3 col-xs-6">
                  <div className="box box-primary">
                     <div className="box-header with-border">
                        <h3 className="box-title">What is this?</h3>
                     </div>
                     <div className="box-body">
                        <p><strong>Should I Water My Garden?</strong> is a Python/React app that I developed to help keep track of the amount of rain.</p>
                        <p>So, should I water my garden?</p>
                        <p>*drumroll*</p>
                        <p><strong>{summaryAnswer}</strong></p>
                        <p>{summaryText}</p>
                     </div>
                  </div>
               </div>
               <div className="col-lg-3 col-xs-6">
                  <div className="small-box bg-green">
                     <div className="inner">
                        <h3>{forecastData}<sup style={{fontSize: 20}}>in</sup></h3>
                        <p>Rain Forecasted For Tomorrow</p>
                     </div>
                     <div className="icon">
                        <i className="fa fas fa-check-square-o"></i>
                     </div>
                  </div>
               </div>
               <div className="col-lg-3 col-xs-6">
                  <div className="small-box bg-green">
                     <div className="inner">
                        <h3>{lastDayData}<sup style={{fontSize: 20}}>in</sup></h3>
                        <p>Rain In The Last Day</p>
                     </div>
                     <div className="icon">
                        <i className="fa fas fa-check-square-o"></i>
                     </div>
                  </div>
               </div>
               <div className="col-lg-3 col-xs-6">
                  <div className="small-box bg-yellow">
                     <div className="inner">
                        <h3>{lastWeekData}<sup style={{fontSize: 20}}>in</sup></h3>
                        <p>Rain In The Last Week</p>
                     </div>
                     <div className="icon">
                        <i className="fa fas fa-check-square-o"></i>
                     </div>
                  </div>
               </div>
            </div>
        );

  }
}
export default HighlightBar;