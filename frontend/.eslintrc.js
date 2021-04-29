module.exports = {
    root: true,
    env: {
        node: true,
    },
    extends: [
        // 'plugin:vue/essential',
        // 'eslint:recommended',
        // '@vue/prettier',
        'plugin:vue/vue3-recommended',
    ],
    rules: {
        // indent: ['error', 4],
    },
    parserOptions: {
        parser: 'babel-eslint',
    },
};
