import { Navigation } from './spa/navigation.js';

const navigation = new Navigation();

navigation.navigateTo(window.location.pathname, document.title);
