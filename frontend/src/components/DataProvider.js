import React, {
    Component
} from "react";
import DataGrid from "./DataGrid";
import Header from "./Header";
import Footer from "./Footer";

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
                    <Header data={this.state.data} />
                    <DataGrid data={this.state.data} />
                    <Footer />
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