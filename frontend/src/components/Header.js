import React from "react";

class Header extends React.Component {
  render() {
    console.log("Header.render");
    console.log(this.props.data);
    var command = this.props.data.summary.should_water_formatted;
    var message = this.props.data.summary.should_water_message;
    if (command){
        return (
            <div class="header-container container-fluid">
               <div class="container">
                  <div class="row">
                     <div class="col-lg-7">
                       <h1>Should I water my garden? <span class="answer">{command}</span></h1>
                       <p>{message}</p>
                     </div>
                  </div>
               </div>
            </div>
        );
    } else {
        return null;
    }
  }
}
export default Header;