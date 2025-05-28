const obj = [
    {img: 'https://media.istockphoto.com/id/1403500817/photo/the-craggies-in-the-blue-ridge-mountains.jpg?s=612x612&w=0&k=20&c=N-pGA8OClRVDzRfj_9AqANnOaDS3devZWwrQNwZuDSk=', title: 'nature'},
    {img: 'https://media.istockphoto.com/id/1403500817/photo/the-craggies-in-the-blue-ridge-mountains.jpg?s=612x612&w=0&k=20&c=N-pGA8OClRVDzRfj_9AqANnOaDS3devZWwrQNwZuDSk=', title: 'nature1'}
];

let html = '';
obj.forEach((item)=> {
    html += `<div class="vedio">
        <div class="img">
            <img src="${item.img}">
        </div>
        <p>${item.title}</p>
    </div>`
})
document.querySelector('.container').innerHTML = html;
