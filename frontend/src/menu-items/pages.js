// assets
import { IconKey, IconSearch } from '@tabler/icons-react';

// constant
const icons = {
  IconKey,
  IconSearch
};

// ==============================|| EXTRA PAGES MENU ITEMS ||============================== //

const pages = {
  id: 'pages',
  title: 'Pages',
  caption: '',
  type: 'group',
  children: [
    // {
    //   id: 'authentication',
    //   title: 'Authentication',
    //   type: 'collapse',
    //   icon: icons.IconKey,

    //   children: [
    //     {
    //       id: 'login3',
    //       title: 'Login',
    //       type: 'item',
    //       url: '/pages/login/login3',
    //       target: true
    //     },
    //     {
    //       id: 'register3',
    //       title: 'Register',
    //       type: 'item',
    //       url: '/pages/register/register3',
    //       target: true
    //     }
    //   ]
    // },
    {
      id: 'scrappers',
      title: 'Scrappers',
      type: 'item',
      icon: icons.IconSearch,
      url:'pages/scrappers'
    }
  ]
};

export default pages;
