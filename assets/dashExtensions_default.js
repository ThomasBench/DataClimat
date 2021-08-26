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
        }
    }
});