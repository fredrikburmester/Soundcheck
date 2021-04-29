module.exports = {
    devServer: {
        host: '0.0.0.0',
        disableHostCheck: true,
        public: `${process.env.VUE_APP_PUBLIC_URL}`,
    },
    lintOnSave: true,
};
