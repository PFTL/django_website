const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const path = require('path');
const sveltePreprocess = require('svelte-preprocess');

const mode = process.env.NODE_ENV || 'development';
const prod = mode === 'production';

module.exports = {
    entry: {
        'build/bundle': ['./assets/main.js']
    },
    resolve: {
        alias: {
            svelte: path.dirname(require.resolve('svelte/package.json'))
        },
        extensions: ['.mjs', '.js', '.svelte'],
        mainFields: ['svelte', 'browser', 'module', 'main']
    },
    output: {
        path: path.join(__dirname, '/pftl/static'),
        publicPath: "/static/",
        filename: '[name].js',
        chunkFilename: '[name]-[id].js'
    },
    module: {
        rules: [
            {
                test: /\.svelte$/,
                use: {
                    loader: 'svelte-loader',
                    options: {
                        compilerOptions: {
                            dev: !prod,
                        },
                        emitCss: prod,
                        hotReload: !prod,
                        preprocess: sveltePreprocess({
                            sourceMap: !prod,
                            postcss:{
                                plugins:[
                                    require("tailwindcss"),
                                    require("postcss-nesting")
                                ]
                            }
                        })
                    }
                }
            },
            {
                test: /\.css$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader'
                ]
            },
            {
                test: /\.html$/,
                loader: "raw-loader"
            },
            {
                // required to prevent errors from Svelte on Webpack 5+
                test: /node_modules\/svelte\/.*\.mjs$/,
                resolve: {
                    fullySpecified: false
                }
            }
        ]
    },
    mode,
    plugins: [
        new MiniCssExtractPlugin({
            filename: '[name].css'
        })
    ],
    devtool: prod ? false : 'source-map',
    devServer: {
        hot: true,
        port: 8081,
        writeToDisk: true,
        watchContentBase: true,
        contentBase: path.resolve(__dirname, "pftl/templates")
    }
};
