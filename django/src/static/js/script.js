import { router } from './spa/navigation.js';
import { getCurrentUser } from './auth.js';

router();

getCurrentUser();
