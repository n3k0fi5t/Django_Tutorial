function keyMirror (obj) {
    if (obj instanceof Object) {
    //   var _obj = Object.assign({}, obj)
      var _obj = JSON.parse(JSON.stringify(obj))
      var _keyArray = Object.keys(obj)
      _keyArray.forEach(key => {
        _obj[key] = key
      })
      return _obj
    }
  }

 export default keyMirror({
     CHANGE_MODAL_STATUS: null,
     UPDATE_WEBSITE_CONF: null,
     CHANGE_PROFILE: null,
     UPDATE_REDIRECT_PATH: null
 })