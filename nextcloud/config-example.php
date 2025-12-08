<?php
$CONFIG = array (
  'instanceid' => '<INSTANCE_ID>',     // 例：ocxxxxxxxxxxxx
  'passwordsalt' => '<PASSWORD_SALT>', // 例：隨機字串
  'secret' => '<NEXTCLOUD_SECRET>',    // 例：長一點的隨機字串
  'trusted_domains' =>
  array (
    0 => 'localhost',
    1 => '192.168.xxx.xxx',        // 或是VPN IP
    2 => '<YOUR_PUBLIC_DOMAIN>',   // 範例：cloud.example.com
  ),
  'datadirectory' => '/srv/nextcloud-data',
  'dbtype' => 'mysql',
  'version' => '32.0.2.2',
  'overwrite.cli.url' => '<YOUR_PUBLIC_DOMAIN>',
  'dbname' => 'nextcloud',
  'dbhost' => 'localhost',
  'dbtableprefix' => 'oc_',
  'mysql.utf8mb4' => true,
  'dbuser' => '<DB_USERNAME>',
  'dbpassword' => '<DB_PASSWORD>',
  'installed' => true,
  'memcache.local' => '\\OC\\Memcache\\APCu',
  'memcache.locking' => '\\OC\\Memcache\\Redis',
  'redis' =>
  array (
    'host' => '127.0.0.1',
    'port' => 6379,
    'timeout' => 1.5,
  ),
  'maintenance' => false,
  'loglevel' => 2,
);
