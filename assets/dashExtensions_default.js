window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, context) {
            const {
                min,
                max,
                colorscale,
                colorProp,
                style
            } = context.props.hideout;
            const csc = chroma.scale(colorscale).domain([min, max]) // chroma lib to construct colorscale
            var color = csc(feature.properties[colorProp])
            style.fillColor = color // set color based on color prop.
            return style // send back the style
        },
        function1: function(feature, latlng) {
            return L.circleMarker(latlng, {
                color: 'black',
                fillOpacity: 1,
                radius: 4,
                fillColor: 'black'
            })
        }
    }
});