import React, {
    Component
} from "react";
import HighlightBar from "./HighlightBar/HighlightBar";
import DataBar from "./DataBar/DataBar";

class DataProvider extends Component {
    state = {
        data: [],
        loaded: false,
        placeholder: "Loading..."
    };
    componentDidMount() {
        console.log("DataProvider.componentDidMount");
        fetch(this.props.endpoint)
            .then(response => {
                if (response.status !== 200) {
                    return this.setState({
                        placeholder: "Something went wrong"
                    });
                }
                console.log(response)
                return response.json();
            })
            .then(data => this.setState({
                data: data,
                loaded: true
            }));
    }
    render() {
        console.log("DataProvider.render");
        if (this.state.loaded) {
            return(
                <div>
                    <HighlightBar data={this.state.data} />
                    <DataBar data={this.state.data} />
                </div>
            )
        } else {
        return (
            <div>
                <p>{this.state.placeholder}</p>
            </div>
            )
        }
    }
}
export default DataProvider;