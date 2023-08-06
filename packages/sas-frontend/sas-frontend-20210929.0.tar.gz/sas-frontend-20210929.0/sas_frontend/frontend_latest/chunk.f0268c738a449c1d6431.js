(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6839],{66839:(e,t,r)=>{"use strict";r.r(t);r(53918);var s=r(55317),i=(r(32296),r(30879),r(15652)),o=r(47181),a=(r(90806),r(52039),r(22814)),n=r(41682),l=r(77097),d=r(26765),c=r(11654);function h(){h=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(s){t.forEach((function(t){var i=t.placement;if(t.kind===s&&("static"===i||"prototype"===i)){var o="static"===i?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var s=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===s?void 0:s.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],s=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!m(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),s.push.apply(s,t.finishers)}),this),!t)return{elements:r,finishers:s};var o=this.decorateConstructor(r,t);return s.push.apply(s,o.finishers),o.finishers=s,o},addElementPlacement:function(e,t,r){var s=t[e.placement];if(!r&&-1!==s.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");s.push(e.key)},decorateElement:function(e,t){for(var r=[],s=[],i=e.decorators,o=i.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var n=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,i[o])(n)||n);e=l.element,this.addElementPlacement(e,t),l.finisher&&s.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);r.push.apply(r,d)}}return{element:e,finishers:s,extras:r}},decorateConstructor:function(e,t){for(var r=[],s=t.length-1;s>=0;s--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[s])(i)||i);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var n=a+1;n<e.length;n++)if(e[a].key===e[n].key&&e[a].placement===e[n].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return g(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?g(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=v(e.key),s=String(e.placement);if("static"!==s&&"prototype"!==s&&"own"!==s)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+s+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:s,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:y(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=y(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var s=(0,t[r])(e);if(void 0!==s){if("function"!=typeof s)throw new TypeError("Finishers must return a constructor.");e=s}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function p(e){var t,r=v(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var s={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(s.decorators=e.decorators),"field"===e.kind&&(s.initializer=e.value),s}function u(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function m(e){return e.decorators&&e.decorators.length}function f(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function y(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function v(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var s=r.call(e,t||"default");if("object"!=typeof s)return s;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function g(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,s=new Array(t);r<t;r++)s[r]=e[r];return s}!function(e,t,r,s){var i=h();if(s)for(var o=0;o<s.length;o++)i=s[o](i);var a=t((function(e){i.initializeInstanceElements(e,n.elements)}),r),n=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},s=0;s<e.length;s++){var i,o=e[s];if("method"===o.kind&&(i=t.find(r)))if(f(o.descriptor)||f(i.descriptor)){if(m(o)||m(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(m(o)){if(m(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}u(o,i)}else t.push(o)}return t}(a.d.map(p)),e);i.initializeClassElements(a.F,n.elements),i.runClassFinishers(a.F,n.finishers)}([(0,i.Mo)("dialog-hassio-snapshot")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,i.sz)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,i.sz)()],key:"_onboarding",value:()=>!1},{kind:"field",decorators:[(0,i.sz)()],key:"_snapshot",value:void 0},{kind:"field",decorators:[(0,i.sz)()],key:"_folders",value:void 0},{kind:"field",decorators:[(0,i.sz)()],key:"_addons",value:void 0},{kind:"field",decorators:[(0,i.sz)()],key:"_dialogParams",value:void 0},{kind:"field",decorators:[(0,i.sz)()],key:"_snapshotPassword",value:void 0},{kind:"field",decorators:[(0,i.sz)()],key:"_restoreHass",value:()=>!0},{kind:"method",key:"showDialog",value:async function(e){var t,r,s,i;this._snapshot=await(0,l.Ju)(this.hass,e.slug),this._folders=(e=>{const t=[];return e.includes("homeassistant")&&t.push({slug:"homeassistant",name:"SmartAutomatic configuration",checked:!0}),e.includes("ssl")&&t.push({slug:"ssl",name:"SSL",checked:!0}),e.includes("share")&&t.push({slug:"share",name:"Share",checked:!0}),e.includes("addons/local")&&t.push({slug:"addons/local",name:"Local add-ons",checked:!0}),t})(null===(t=this._snapshot)||void 0===t?void 0:t.folders).sort(((e,t)=>e.name>t.name?1:-1)),this._addons=(i=null===(r=this._snapshot)||void 0===r?void 0:r.addons,i.map((e=>({slug:e.slug,name:e.name,version:e.version,checked:!0})))).sort(((e,t)=>e.name>t.name?1:-1)),this._dialogParams=e,this._onboarding=null!==(s=e.onboarding)&&void 0!==s&&s}},{kind:"method",key:"render",value:function(){return this._dialogParams&&this._snapshot?i.dy`
      <ha-dialog open @closing=${this._closeDialog} .heading=${!0}>
        <div slot="heading">
          <ha-header-bar>
            <span slot="title">
              ${this._computeName}
            </span>
            <mwc-icon-button slot="actionItems" dialogAction="cancel">
              <ha-svg-icon .path=${s.r5M}></ha-svg-icon>
            </mwc-icon-button>
          </ha-header-bar>
        </div>
        <div class="details">
          ${"full"===this._snapshot.type?"Full snapshot":"Partial snapshot"}
          (${this._computeSize})<br />
          ${this._formatDatetime(this._snapshot.date)}
        </div>
        <div>SmartAutomatic:</div>
        <paper-checkbox
          .checked=${this._restoreHass}
          @change="${e=>{this._restoreHass=e.target.checked}}"
        >
          SmartAutomatic ${this._snapshot.homeassistant}
        </paper-checkbox>
        ${this._folders.length?i.dy`
              <div>Folders:</div>
              <paper-dialog-scrollable class="no-margin-top">
                ${this._folders.map((e=>i.dy`
                    <paper-checkbox
                      .checked=${e.checked}
                      @change="${t=>this._updateFolders(e,t.target.checked)}"
                    >
                      ${e.name}
                    </paper-checkbox>
                  `))}
              </paper-dialog-scrollable>
            `:""}
        ${this._addons.length?i.dy`
              <div>Add-on:</div>
              <paper-dialog-scrollable class="no-margin-top">
                ${this._addons.map((e=>i.dy`
                    <paper-checkbox
                      .checked=${e.checked}
                      @change="${t=>this._updateAddons(e,t.target.checked)}"
                    >
                      ${e.name}
                    </paper-checkbox>
                  `))}
              </paper-dialog-scrollable>
            `:""}
        ${this._snapshot.protected?i.dy`
              <paper-input
                autofocus=""
                label="Password"
                type="password"
                @value-changed=${this._passwordInput}
                .value=${this._snapshotPassword}
              ></paper-input>
            `:""}
        ${this._error?i.dy` <p class="error">Error: ${this._error}</p> `:""}

        <div class="button-row" slot="primaryAction">
          <mwc-button @click=${this._partialRestoreClicked}>
            <ha-svg-icon .path=${s.BBX} class="icon"></ha-svg-icon>
            Restore Selected
          </mwc-button>
          ${this._onboarding?"":i.dy`
                <mwc-button @click=${this._deleteClicked}>
                  <ha-svg-icon .path=${s.x9U} class="icon warning">
                  </ha-svg-icon>
                  <span class="warning">Delete Snapshot</span>
                </mwc-button>
              `}
        </div>
        <div class="button-row" slot="secondaryAction">
          ${"full"===this._snapshot.type?i.dy`
                <mwc-button @click=${this._fullRestoreClicked}>
                  <ha-svg-icon .path=${s.BBX} class="icon"></ha-svg-icon>
                  Restore Everything
                </mwc-button>
              `:""}
          ${this._onboarding?"":i.dy`<mwc-button @click=${this._downloadClicked}>
                <ha-svg-icon .path=${s.OGU} class="icon"></ha-svg-icon>
                Download Snapshot
              </mwc-button>`}
        </div>
      </ha-dialog>
    `:i.dy``}},{kind:"get",static:!0,key:"styles",value:function(){return[c.Qx,c.yu,i.iv`
        paper-checkbox {
          display: block;
          margin: 4px;
        }
        mwc-button ha-svg-icon {
          margin-right: 4px;
        }
        .button-row {
          display: grid;
          gap: 8px;
          margin-right: 8px;
        }
        .details {
          color: var(--secondary-text-color);
        }
        .warning,
        .error {
          color: var(--error-color);
        }
        .buttons li {
          list-style-type: none;
        }
        .buttons .icon {
          margin-right: 16px;
        }
        .no-margin-top {
          margin-top: 0;
        }
        ha-header-bar {
          --mdc-theme-on-primary: var(--primary-text-color);
          --mdc-theme-primary: var(--mdc-theme-surface);
          flex-shrink: 0;
        }
        /* overrule the ha-style-dialog max-height on small screens */
        @media all and (max-width: 450px), all and (max-height: 500px) {
          ha-header-bar {
            --mdc-theme-primary: var(--app-header-background-color);
            --mdc-theme-on-primary: var(--app-header-text-color, white);
          }
        }
      `]}},{kind:"method",key:"_updateFolders",value:function(e,t){this._folders=this._folders.map((r=>(r.slug===e.slug&&(r.checked=t),r)))}},{kind:"method",key:"_updateAddons",value:function(e,t){this._addons=this._addons.map((r=>(r.slug===e.slug&&(r.checked=t),r)))}},{kind:"method",key:"_passwordInput",value:function(e){this._snapshotPassword=e.detail.value}},{kind:"method",key:"_partialRestoreClicked",value:async function(){if(!await(0,d.g7)(this,{title:"Are you sure you want partially to restore this snapshot?",confirmText:"restore",dismissText:"cancel"}))return;const e=this._addons.filter((e=>e.checked)).map((e=>e.slug)),t=this._folders.filter((e=>e.checked)).map((e=>e.slug)),r={homeassistant:this._restoreHass,addons:e,folders:t};this._snapshot.protected&&(r.password=this._snapshotPassword),this._onboarding?((0,o.B)(this,"restoring"),fetch(`/api/hassio/snapshots/${this._snapshot.slug}/restore/partial`,{method:"POST",body:JSON.stringify(r)}),this._closeDialog()):this.hass.callApi("POST",`hassio/snapshots/${this._snapshot.slug}/restore/partial`,r).then((()=>{alert("Snapshot restored!"),this._closeDialog()}),(e=>{this._error=e.body.message}))}},{kind:"method",key:"_fullRestoreClicked",value:async function(){if(!await(0,d.g7)(this,{title:"Are you sure you want to wipe your system and restore this snapshot?",confirmText:"restore",dismissText:"cancel"}))return;const e=this._snapshot.protected?{password:this._snapshotPassword}:void 0;this._onboarding?((0,o.B)(this,"restoring"),fetch(`/api/hassio/snapshots/${this._snapshot.slug}/restore/full`,{method:"POST",body:JSON.stringify(e)}),this._closeDialog()):this.hass.callApi("POST",`hassio/snapshots/${this._snapshot.slug}/restore/full`,e).then((()=>{alert("Snapshot restored!"),this._closeDialog()}),(e=>{this._error=e.body.message}))}},{kind:"method",key:"_deleteClicked",value:async function(){await(0,d.g7)(this,{title:"Are you sure you want to delete this snapshot?",confirmText:"delete",dismissText:"cancel"})&&this.hass.callApi("POST",`hassio/snapshots/${this._snapshot.slug}/remove`).then((()=>{this._dialogParams.onDelete&&this._dialogParams.onDelete(),this._closeDialog()}),(e=>{this._error=e.body.message}))}},{kind:"method",key:"_downloadClicked",value:async function(){let e;try{e=await(0,a.iI)(this.hass,`/api/hassio/snapshots/${this._snapshot.slug}/download`)}catch(e){return void alert("Error: "+(0,n.js)(e))}if(window.location.href.includes("ui.nabu.casa")){if(!await(0,d.g7)(this,{title:"Potential slow download",text:"Downloading snapshots over the Nabu Casa URL will take some time, it is recomended to use your local URL instead, do you want to continue?",confirmText:"continue",dismissText:"cancel"}))return}const t=this._computeName.replace(/[^a-z0-9]+/gi,"_"),r=document.createElement("a");r.href=e.path,r.download=`Hass_io_${t}.tar`,this.shadowRoot.appendChild(r),r.click(),this.shadowRoot.removeChild(r)}},{kind:"get",key:"_computeName",value:function(){return this._snapshot?this._snapshot.name||this._snapshot.slug:"Unnamed snapshot"}},{kind:"get",key:"_computeSize",value:function(){return Math.ceil(10*this._snapshot.size)/10+" MB"}},{kind:"method",key:"_formatDatetime",value:function(e){return new Date(e).toLocaleDateString(navigator.language,{weekday:"long",year:"numeric",month:"short",day:"numeric",hour:"numeric",minute:"2-digit"})}},{kind:"method",key:"_closeDialog",value:function(){this._dialogParams=void 0,this._snapshot=void 0,this._snapshotPassword="",this._folders=[],this._addons=[]}}]}}),i.oi)}}]);
//# sourceMappingURL=chunk.f0268c738a449c1d6431.js.map