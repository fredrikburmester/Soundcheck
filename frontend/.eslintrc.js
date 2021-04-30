module.exports = {
    root: true,
    env: {
        browser: true,
        node: false,
        es6: true
    },
    extends: [
        'plugin:vue/vue3-recommended',
    ],
    plugins: [
        'prettier',
        'vue'   
    ],
    parserOptions: {
        "parser": 'babel-eslint',
        "sourceType": "module",
    },
    rules: {
        "vue/max-attributes-per-line": ["error", {
            "singleline": 5,      
            "multiline": 5
        }],
        "vue/script-indent": ["error", 4],
        "vue/html-indent": ["error", 4],
        "indent": ["error", 4],
    }
};
