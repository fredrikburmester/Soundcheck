<template>
    <div class="aboutPage">
        
        <h1>About Soundcheck</h1>
        <div class="text">
            <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                Etiam tristique massa lectus, id maximus velit vulputate at.
                Aenean eget arcu sapien.
                Sed ut ipsum sit amet enim tincidunt viverra et ut arcu. 
                Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae;
                Sed quis mauris a dolor vehicula accumsan.
                Phasellus vel urna nibh. Praesent hendrerit in ipsum in mollis.
                <br>
                <br>
                Quisque ultricies, arcu ac eleifend finibus, quam enim vulputate est,
                vitae scelerisque felis leo vitae purus. Praesent commodo est felis,
                sed luctus libero hendrerit nec. In sem ante, faucibus non tellus eget,
                fringilla rhoncus tortor. Class aptent taciti sociosqu ad litora torquent
                per conubia nostra, per inceptos himenaeos. Phasellus ut ante eu lacus
                auctor mollis at quis ex. Donec posuere sit amet metus vitae lobortis.
                Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            </p>
        </div>
        <Button 
            button-link="/" 
            button-text="Back"
            color="#CD1A2B"
        />
    </div>
</template>

<script>
import Button from '../components/Button'

export default {
    name: 'About',
    components: {
        Button,
    },

};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');
.aboutPage{
    font-family: 'Roboto', sans-serif;
    display: inline-block;
    margin: 50px 10px 50px 10px;
    width: 80vw;
}
.text{
    margin: 50px 20px 50px 20px;
    font-weight: 300;
}

</style>