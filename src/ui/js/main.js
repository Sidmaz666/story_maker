// Init Tiny MCE Function
function initTiny(){
    tinymce.remove()
    tinymce.init({
  	selector: '#compile-text',
	plugins: 'fullscreen searchreplace autolink directionality visualblocks visualchars image link media codesample charmap pagebreak nonbreaking anchor insertdatetime advlist lists wordcount charmap emoticons autosave',
	toolbar: 'undo redo | blocks fontfamily fontsize | bold italic underline forecolor backcolor | link image | alignleft aligncenter alignright alignjustify lineheight | bullist numlist indent | removeformat',
      height: '500px',
      skin: localStorage.getItem('theme') == "dark" ? "bootstrap" : "oxide",
      content_css: localStorage.getItem('theme') == "dark"  ? "tinymce-5-dark" : "default",
    });
    setInterval(() => {
      if(document.querySelector('.tox-promotion')) document.querySelector('.tox-promotion').remove()
      if(document.querySelector('.tox-statusbar__branding')) document.querySelector('.tox-statusbar__branding').remove()
    },800)
}

// Toggle Color Mode
function toggleColorMode(btn){
  const current_value=document.querySelector('html').getAttribute("data-bs-theme")
  if(current_value == "dark"){
	document.querySelector('html').setAttribute("data-bs-theme", "light")
	localStorage.setItem("theme", "light")
    	btn.innerHTML = `<i class="fa-solid fa-moon"></i>`
  } else {
	document.querySelector('html').setAttribute("data-bs-theme", "dark")
	localStorage.setItem("theme", "dark")
    	btn.innerHTML = `<i class="fa-solid fa-sun"></i>`
  }
  // Refresh Tiny MCE
  initTiny()
}

window.onload = async function(){
  // Set Color Mode From Local Storage
  // Default Dark Mode
  localStorage.setItem("theme", localStorage.getItem("theme") || "dark")
  color_mode = localStorage.getItem("theme")
  if(color_mode == "light"){
      document.querySelector('#toggle-color-btn').innerHTML=`<i class="fa-solid fa-moon"></i>`
  } else {
      document.querySelector('#toggle-color-btn').innerHTML=`<i class="fa-solid fa-sun"></i>`
  }
  document.querySelector('html').setAttribute("data-bs-theme", color_mode)
  // Init Model & Sampler
  const {data} = await axios.get("/api/list")
  const {models,sampler,default_model,default_sampler} = data
  models.forEach((e) => {
    document.querySelector('#image-model').insertAdjacentHTML("beforeend", `
	  <option value="${e}" ${e == default_model ? 'selected' : ''}>${e}</option>
      `)
    // Init Tiny MCE
    initTiny()
  })
  sampler.forEach((e) => {
    document.querySelector('#image-sample').insertAdjacentHTML("beforeend", `
	  <option value="${e}" ${e == default_sampler ? 'selected' : ''}>${e}</option>
      `)
  })
}

// TextArea Resize  

function TextAreaResize(textarea){
	  textarea.style.height = 'auto';
	  textarea.style.height = textarea.scrollHeight + 'px';
	  textarea.style.overflow = 'hidden';
	  textarea.style.resize = 'none';
}

function autoTextAreaResize(textarea) {
  	  TextAreaResize(textarea)
	  textarea.addEventListener('input', function(){
	    TextAreaResize(textarea)
	  } , false);
}

// Function To Copy Text Onto Clipboard
function copy2clipboard(id){
  const from = document.querySelector(`#${id}`)
  from.select();
  from.setSelectionRange(0, 99999);
  navigator.clipboard.writeText(from.value);
  window.getSelection().removeAllRanges()
}

// Function to Download image
function download_img(url){
      const downloadLink = document.createElement('a');
      downloadLink.href = url;
      downloadLink.download = 'image.png';
      document.body.appendChild(downloadLink);
      downloadLink.click();
      document.body.removeChild(downloadLink);
} 

// Global variable to store images data uri
const IMGS = []

// Function To Add Image in the Queue
function add2queue(btn,url){
  	btn.disabled = true
  	btn.innerHTML = `
		  <span>Added</span> <i class="fa-solid fa-check"></i>
  	`
	IMGS.push(url)
	// Show Added Images in the Compile Section
	document.querySelector("#added-images").innerHTML = ""
	IMGS.forEach((e) => {
		document.querySelector("#added-images").insertAdjacentHTML("beforeend",`
		<img src="${e}" style="height:80px;width:80px;cursor:grab"
		class="m-2 img-thumbnail" alt="added_image">
		  `)
	})
}

function reset_queue_btn(btn){
	btn.disabled = false
  	btn.innerHTML = `
		  <span>Add</span> <i class="fa-solid fa-plus"></i>
  	`
}

// Standard API Call Function
async function get(endpoint,prompt){
  try {
	const {data} = await axios.post(`/api/${endpoint}`,{ prompt:prompt })
    	return data.data
  } catch (error) {
  	console.log(error)
  }
}

async function standard_process(type,prompt,btn,endpoint,remove,pre_data=""){
    if(typeof prompt == "string" && prompt.length >= 1 || typeof prompt == "object"){
      // Disable Button
      if(btn) btn.disabled = true
      // Show Loader
      document.getElementById(`${type}-loader`).classList.remove("visually-hidden")
      // check if Image
      if(type !== "image"){
      // Get Data
      const generated = await get(endpoint,prompt)
      document.getElementById(`generated-${type}`).value = pre_data + generated?.replace(remove,"").replace(/^\n+/,"").replace(/^\s+/,"")
      } else if(type == "image" && typeof prompt == "object"){
	if(!document.querySelector(`.generated-${type}-container`).getAttribute("class").includes("visually-hidden")){
	  document.querySelector(`.generated-${type}-container`).classList.add("visually-hidden")
	}
	const req = await axios.post(`/api/${endpoint}`,prompt)
	const response = await axios.get(await req.data.url, { responseType: 'arraybuffer' });
	 const base64Image = btoa(new Uint8Array(response.data)
	   .reduce((data, byte) => data + String.fromCharCode(byte), ''));
	const dataURL = `data:${response.headers['content-type']};base64,${base64Image}`;
	document.querySelector(`#${type}-output`).src = dataURL
      }
      // Enable Button
      if(btn) btn.disabled = false
      // Hide Loader
      document.getElementById(`${type}-loader`).classList.add("visually-hidden")
      // Show Text Area
      document.querySelector(`.generated-${type}-container`).classList.remove("visually-hidden")
      if(type !== "image"){
      // Resize Text Area According to the Content
      autoTextAreaResize(document.getElementById(`generated-${type}`))
      }
    }
}

// Plot Form Data Process
document.forms['plot_form'].addEventListener('submit', async function(e) {
    e.preventDefault();
    const plot_prompt = document.forms['plot_form']['plot_prompt'].value
    const plot_btn = document.forms['plot_form']['plot_btn']
    await standard_process("plot", plot_prompt, plot_btn,"plot","Plot:")
})

// Story Form Data Process
document.forms['story_form'].addEventListener('submit', async function(e) {
    e.preventDefault();
    const story_prompt = document.forms['story_form']['story_prompt'].value
    const story_btn = document.forms['story_form']['story_btn']
    await standard_process("story", story_prompt, story_btn,"story","Story:")
})

// Continue Rewrite Story
async function continue_story(btn){
      const story_container = document.querySelector("#generated-story")
      const _story = story_container.value
      // Hide Text Area
      document.querySelector(".generated-story-container").classList.add("visually-hidden")
      standard_process("story", _story, btn,"continue","Story:",`${_story}\n\n------------------\n\n`)
}

// Characters From Data Process
document.forms['character_form'].addEventListener('submit', async function(e) {
    e.preventDefault();
    const character_prompt = document.forms['character_form']['character_prompt'].value
    const character_btn = document.forms['character_form']['character_btn']
    await standard_process("character", character_prompt, character_btn,"character","")
})

// Character Detail From Data Process
document.forms['character_detail_form'].addEventListener('submit', async function(e) {
    e.preventDefault();
    const character_detail_prompt = document.forms['character_detail_form']['character_detail_prompt'].value
    const character_detail_btn = document.forms['character_detail_form']['character_detail_btn']
    await standard_process("character-detail", character_detail_prompt, character_detail_btn,"character_detail","CharacterDetail:")
})

// Environment From Data Process
document.forms['environment_form'].addEventListener('submit', async function(e) {
    e.preventDefault();
    const environment_prompt = document.forms['environment_form']['environment_prompt'].value
    const environment_btn = document.forms['environment_form']['environment_btn']
    await standard_process("environment", environment_prompt, environment_btn,"environment","")
})

// Image Form Data Process
document.forms['image_form'].addEventListener('submit', async function(e) {
    e.preventDefault();
    const image_btn = document.forms['image_form']['image_btn']
    const formData = new FormData(this);

    let formValues = {};
    formData.forEach((value, key) => {
      formValues[key] = value;
    });

    const jsonFormData = formValues;
    if(jsonFormData.image_prompt.length >= 2){
      await standard_process("image", jsonFormData,image_btn, "img")
    }
})

// Custom From Data Process
document.forms['custom_form'].addEventListener('submit', async function(e) {
    e.preventDefault();
    const custom_prompt = document.forms['custom_form']['custom_prompt'].value
    const custom_btn = document.forms['custom_form']['custom_btn']
    await standard_process("custom", custom_prompt, custom_btn,"custom","")
})

