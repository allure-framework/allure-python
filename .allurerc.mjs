export default {
  name: "Allure Python",
  output: "./out/allure-report",
  plugins: {
    testops: {
      options: {
        launchName: `Allure Python GitHub actions run (${new Date().toISOString()})`,
      },
    },
  },
};
