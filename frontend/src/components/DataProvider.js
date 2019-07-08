import React, {
    Component
} from "react";

class DataProvider extends Component {
    state = {
        data: [],
        source: "endpoint",
        loaded: false,
        placeholder: "Loading..."
    };
    componentDidMount() {
        if (this.props.source == "file") {
            // TODO: make sure this works
            this.setState({ data: this.json_data, loaded: true });
            return this.json_data;

        } else if (this.props.source == "api") {

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
    }
    render() {
        const {
            data,
            loaded,
            placeholder
        } = this.state;
        return loaded ? this.props.render(data) : < p > {
            placeholder
        } < /p>;
    }
}
export default DataProvider;