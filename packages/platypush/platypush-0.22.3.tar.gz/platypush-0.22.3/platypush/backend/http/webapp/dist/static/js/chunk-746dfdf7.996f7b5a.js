(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-746dfdf7"],{"2a628":function(e,t,r){"use strict";r.r(t);r("38cf"),r("ac1f"),r("841c");var n=r("7a23");function a(e,t,r,a,s,i){var c=Object(n["z"])("Loading"),u=Object(n["z"])("MusicPlugin");return Object(n["r"])(),Object(n["e"])(n["a"],null,[s.loading?(Object(n["r"])(),Object(n["e"])(c,{key:0})):Object(n["f"])("",!0),Object(n["h"])(u,{"plugin-name":"music.spotify",loading:s.loading,config:r.config,tracks:s.tracks,status:s.status,playlists:s.playlists,"edited-playlist":s.editedPlaylist,"edited-playlist-tracks":s.editedPlaylistTracks,"track-info":s.trackInfo,"search-results":s.searchResults,"library-results":s.libraryResults,path:s.path,devices:s.devices,"selected-device":s.selectedDevice,"active-device":s.activeDevice,onPlay:i.play,onPause:i.pause,onStop:i.stop,onPrevious:i.previous,onNext:i.next,onClear:i.clear,onSetVolume:i.setVolume,onSeek:i.seek,onConsume:i.consume,onRandom:i.random,onRepeat:i.repeat,onStatusUpdate:t[1]||(t[1]=function(e){return i.refreshStatus(!0)}),onNewPlayingTrack:t[2]||(t[2]=function(e){return i.refreshStatus(!0)}),onRemoveFromTracklist:i.removeFromTracklist,onAddToTracklist:i.addToTracklist,onSwapTracks:i.swapTracks,onLoadPlaylist:i.loadPlaylist,onPlayPlaylist:i.playPlaylist,onRemovePlaylist:i.removePlaylist,onTracklistMove:i.moveTracklistTracks,onTracklistSave:i.saveToPlaylist,onPlaylistEdit:i.playlistEditChanged,onRefreshStatus:i.refreshStatus,onAddToTracklistFromEditedPlaylist:i.addToTracklistFromEditedPlaylist,onRemoveFromPlaylist:i.removeFromPlaylist,onInfo:t[3]||(t[3]=function(e){return s.trackInfo=e}),onPlaylistAdd:i.playlistAdd,onAddToPlaylist:i.addToPlaylist,onPlaylistTrackMove:i.playlistTrackMove,onSearch:i.search,onSearchClear:t[4]||(t[4]=function(e){return s.searchResults=[]}),onCd:i.cd,onPlaylistUpdate:t[5]||(t[5]=function(e){return i.refresh(!0)}),onSelectDevice:i.selectDevice},null,8,["loading","config","tracks","status","playlists","edited-playlist","edited-playlist-tracks","track-info","search-results","library-results","path","devices","selected-device","active-device","onPlay","onPause","onStop","onPrevious","onNext","onClear","onSetVolume","onSeek","onConsume","onRandom","onRepeat","onRemoveFromTracklist","onAddToTracklist","onSwapTracks","onLoadPlaylist","onPlayPlaylist","onRemovePlaylist","onTracklistMove","onTracklistSave","onPlaylistEdit","onRefreshStatus","onAddToTracklistFromEditedPlaylist","onRemoveFromPlaylist","onPlaylistAdd","onAddToPlaylist","onPlaylistTrackMove","onSearch","onCd","onSelectDevice"])],64)}var s=r("5530"),i=r("2909"),c=r("1da1"),u=(r("96cf"),r("d81d"),r("4de4"),r("07ac"),r("99af"),r("4e82"),r("b0c0"),r("d3b7"),r("3ca3"),r("ddb0"),r("0d41")),o=r("3e54"),l=r("3a5e"),d={name:"MusicSpotify",components:{Loading:l["a"],MusicPlugin:u["default"]},mixins:[o["a"]],props:{config:{type:Object,default:function(){}}},data:function(){return{loading:!1,devices:{},selectedDevice:null,activeDevice:null,tracks:[],playlists:[],status:{},editedPlaylist:null,editedPlaylistTracks:[],trackInfo:null,searchResults:[],libraryResults:[],path:"/"}},methods:{refreshTracks:function(e){var t=this;return Object(c["a"])(regeneratorRuntime.mark((function r(){return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:return e||(t.loading=!0),r.prev=1,r.next=4,t.request("music.spotify.history");case 4:t.tracks=r.sent.map((function(e){return e.time=e.duration,e}));case 5:return r.prev=5,t.loading=!1,r.finish(5);case 8:case"end":return r.stop()}}),r,null,[[1,,5,8]])})))()},refreshStatus:function(e){var t=this;return Object(c["a"])(regeneratorRuntime.mark((function r(){var n,a,c,u;return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:return e||(t.loading=!0),r.next=3,t.request("music.spotify.get_devices");case 3:return t.devices=r.sent.reduce((function(e,t){return e[t.id]=t,e}),{}),n=Object.values(t.devices).filter((function(e){return e.is_active})),t.activeDevice=n.length?n[0].id:null,!t.selectedDevice&&Object.values(t.devices).length&&(t.selectedDevice=t.activeDevice||Object(i["a"])(Object.values(t.devices))[0].id),r.prev=7,r.next=10,t.request("music.spotify.status");case 10:a=r.sent,t.status=Object(s["a"])(Object(s["a"])({},a),{},{duration:a.time});case 12:return r.prev=12,t.loading=!1,r.finish(12);case 15:t.status.track&&((null===(c=t.tracks)||void 0===c||null===(u=c[0])||void 0===u?void 0:u.id)!==t.status.track.id&&(t.tracks=[Object(s["a"])(Object(s["a"])({},t.status.track),{},{time:t.status.duration})].concat(Object(i["a"])(t.tracks))),t.status.playingPos=0);case 16:case"end":return r.stop()}}),r,null,[[7,,12,15]])})))()},refreshPlaylists:function(e){var t=this;return Object(c["a"])(regeneratorRuntime.mark((function r(){return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:return e||(t.loading=!0),r.prev=1,r.next=4,t.request("music.spotify.get_playlists");case 4:t.playlists=r.sent.sort((function(e,t){return e.name.localeCompare(t.name)}));case 5:return r.prev=5,t.loading=!1,r.finish(5);case 8:case"end":return r.stop()}}),r,null,[[1,,5,8]])})))()},refresh:function(e){var t=this;return Object(c["a"])(regeneratorRuntime.mark((function r(){return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:return e||(t.loading=!0),r.prev=1,r.next=4,Promise.all([t.refreshTracks(e),t.refreshStatus(e),t.refreshPlaylists(e)]);case 4:return r.prev=4,t.loading=!1,r.finish(4);case 7:case"end":return r.stop()}}),r,null,[[1,,4,7]])})))()},play:function(e){var t=this;return Object(c["a"])(regeneratorRuntime.mark((function r(){return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:if(null!=(null===e||void 0===e?void 0:e.pos)&&(e.uri=t.tracks[e.pos].uri),null===e||void 0===e||!e.uri){r.next=6;break}return r.next=4,t.request("music.spotify.play",{resource:e.uri,device:t.selectedDevice});case 4:r.next=8;break;case 6:return r.next=8,t.request("music.spotify.play",{device:t.selectedDevice});case 8:return r.next=10,t.refreshStatus(!0);case 10:case"end":return r.stop()}}),r)})))()},pause:function(){var e=this;return Object(c["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.next=2,e.request("music.spotify.pause",{device:e.selectedDevice});case 2:return t.next=4,e.refreshStatus(!0);case 4:case"end":return t.stop()}}),t)})))()},stop:function(){var e=this;return Object(c["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.next=2,e.request("music.spotify.stop",{device:e.selectedDevice});case 2:return t.next=4,e.refreshStatus(!0);case 4:case"end":return t.stop()}}),t)})))()},previous:function(){var e=this;return Object(c["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.next=2,e.request("music.spotify.previous",{device:e.selectedDevice});case 2:return t.next=4,e.refreshStatus(!0);case 4:case"end":return t.stop()}}),t)})))()},next:function(){var e=this;return Object(c["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.next=2,e.request("music.spotify.next",{device:e.selectedDevice});case 2:return t.next=4,e.refreshStatus(!0);case 4:case"end":return t.stop()}}),t)})))()},clear:function(){return Object(c["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:case"end":return e.stop()}}),e)})))()},setVolume:function(e){var t=this;return Object(c["a"])(regeneratorRuntime.mark((function r(){return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:if(e!==t.status.volume){r.next=2;break}return r.abrupt("return");case 2:return r.next=4,t.request("music.spotify.set_volume",{device:t.selectedDevice,volume:e});case 4:return r.next=6,t.refreshStatus(!0);case 6:case"end":return r.stop()}}),r)})))()},seek:function(e){var t=this;return Object(c["a"])(regeneratorRuntime.mark((function r(){return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:return r.next=2,t.request("music.spotify.seek",{device:t.selectedDevice,position:e});case 2:return r.next=4,t.refreshStatus(!0);case 4:case"end":return r.stop()}}),r)})))()},repeat:function(){var e=this;return Object(c["a"])(regeneratorRuntime.mark((function t(){var r;return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.next=2,e.request("music.spotify.repeat",{device:e.selectedDevice,value:!(null!==(r=e.status)&&void 0!==r&&r.repeat)});case 2:return t.next=4,e.refreshStatus(!0);case 4:case"end":return t.stop()}}),t)})))()},random:function(){var e=this;return Object(c["a"])(regeneratorRuntime.mark((function t(){var r;return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.next=2,e.request("music.spotify.random",{device:e.selectedDevice,value:!(null!==(r=e.status)&&void 0!==r&&r.random)});case 2:return t.next=4,e.refreshStatus(!0);case 4:case"end":return t.stop()}}),t)})))()},consume:function(){return Object(c["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:case"end":return e.stop()}}),e)})))()},addToTracklist:function(e){var t=this;return Object(c["a"])(regeneratorRuntime.mark((function r(){return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:return e.file&&(e=e.file),r.next=3,t.request("music.spotify.add",{device:t.selectedDevice,resource:e});case 3:return r.next=5,t.refresh(!0);case 5:case"end":return r.stop()}}),r)})))()},addToTracklistFromEditedPlaylist:function(e){var t=this;return Object(c["a"])(regeneratorRuntime.mark((function r(){var n,a;return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:if(n=t.editedPlaylistTracks[e.pos],n){r.next=3;break}return r.abrupt("return");case 3:return a=e.play?"play":"add",r.next=6,t.request("music.spotify.".concat(a),{device:t.selectedDevice,resource:n.uri});case 6:return r.next=8,t.refresh(!0);case 8:case"end":return r.stop()}}),r)})))()},removeFromPlaylist:function(e){var t=this;return Object(c["a"])(regeneratorRuntime.mark((function r(){var n;return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:return n=e.map((function(e){return t.playlists[t.editedPlaylist].tracks[e].uri})),r.next=3,t.request("music.spotify.remove_from_playlist",{resources:n,playlist:t.playlists[t.editedPlaylist].name});case 3:return r.next=5,t.playlistEditChanged(t.editedPlaylist);case 5:case"end":return r.stop()}}),r)})))()},removeFromTracklist:function(){return Object(c["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:case"end":return e.stop()}}),e)})))()},swapTracks:function(){return Object(c["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:case"end":return e.stop()}}),e)})))()},playPlaylist:function(e){var t=this;return Object(c["a"])(regeneratorRuntime.mark((function r(){return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:return r.next=2,t._loadPlaylist(e,!0);case 2:case"end":return r.stop()}}),r)})))()},loadPlaylist:function(e){var t=this;return Object(c["a"])(regeneratorRuntime.mark((function r(){return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:return r.next=2,t._loadPlaylist(e,!1);case 2:case"end":return r.stop()}}),r)})))()},_loadPlaylist:function(e){var t=this;return Object(c["a"])(regeneratorRuntime.mark((function r(){var n;return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:return n=t.playlists[e],r.next=3,t.request("music.spotify.play",{resource:n.uri,device:t.selectedDevice});case 3:return r.next=5,t.refresh(!0);case 5:case"end":return r.stop()}}),r)})))()},removePlaylist:function(){var e=this;return Object(c["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:e.notify({text:"Playlist removal is not supported"});case 1:case"end":return t.stop()}}),t)})))()},saveToPlaylist:function(){return Object(c["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:case"end":return e.stop()}}),e)})))()},moveTracklistTracks:function(){return Object(c["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:case"end":return e.stop()}}),e)})))()},playlistAdd:function(e){var t=this;return Object(c["a"])(regeneratorRuntime.mark((function r(){return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:return r.next=2,t.request("music.spotify.add_to_playlist",{resources:[e],playlist:t.playlists[t.editedPlaylist].uri});case 2:return r.next=4,t.playlistEditChanged(t.editedPlaylist);case 4:case"end":return r.stop()}}),r)})))()},playlistEditChanged:function(e){var t=this;return Object(c["a"])(regeneratorRuntime.mark((function r(){var n;return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:if(t.editedPlaylist=e,null!=e){r.next=3;break}return r.abrupt("return");case 3:return t.loading=!0,r.prev=4,r.next=7,t.request("music.spotify.get_playlist",{playlist:t.playlists[e].uri});case 7:n=r.sent,t.editedPlaylistTracks=n.tracks.map((function(e){return e.time=e.duration,e}));case 9:return r.prev=9,t.loading=!1,r.finish(9);case 12:case"end":return r.stop()}}),r,null,[[4,,9,12]])})))()},addToPlaylist:function(e){var t=this;return Object(c["a"])(regeneratorRuntime.mark((function r(){return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:return r.next=2,Promise.all(e.playlists.map(function(){var r=Object(c["a"])(regeneratorRuntime.mark((function r(n){return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:return r.next=2,t.request("music.spotify.add_to_playlist",{resources:[e.track.uri],playlist:t.playlists[n].uri});case 2:return r.next=4,t.playlistEditChanged(n);case 4:case"end":return r.stop()}}),r)})));return function(e){return r.apply(this,arguments)}}()));case 2:case"end":return r.stop()}}),r)})))()},playlistTrackMove:function(e){var t=this;return Object(c["a"])(regeneratorRuntime.mark((function r(){return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:return r.next=2,t.request("music.spotify.playlist_move",{playlist:t.playlists[e.playlist].uri,from_pos:e.from-1,to_pos:e.to-1});case 2:return r.next=4,t.playlistEditChanged(e.playlist);case 4:case"end":return r.stop()}}),r)})))()},search:function(e){var t=this;return Object(c["a"])(regeneratorRuntime.mark((function r(){return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:return t.loading=!0,r.prev=1,r.next=4,t.request("music.spotify.search",e);case 4:t.searchResults=r.sent.map((function(e){return e.time=e.duration,e}));case 5:return r.prev=5,t.loading=!1,r.finish(5);case 8:case"end":return r.stop()}}),r,null,[[1,,5,8]])})))()},cd:function(){return Object(c["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:case"end":return e.stop()}}),e)})))()},selectDevice:function(e){var t=this;return Object(c["a"])(regeneratorRuntime.mark((function r(){return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:if(t.selectedDevice!==e){r.next=2;break}return r.abrupt("return");case 2:return r.next=4,t.request("music.spotify.start_or_transfer_playback",{device:e});case 4:t.selectedDevice=e,t.refreshStatus(!0);case 6:case"end":return r.stop()}}),r)})))()}},mounted:function(){this.refresh()}};d.render=a;t["default"]=d}}]);
//# sourceMappingURL=chunk-746dfdf7.996f7b5a.js.map