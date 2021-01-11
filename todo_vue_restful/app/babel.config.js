module.exports = {
  presets: [
    '@vue/cli-plugin-babel/preset',
    ["env", {
      "modules": false,
      "targets": {
        "browsers": ["> 1%", "last 2 versions", "not ie <= 9"]
      },
      "useBuiltIns": true
    }],
  ]
}
