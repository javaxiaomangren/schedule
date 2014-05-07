
CREATE TABLE company(
  id INT(11) NOT NULL AUTO_INCREMENT,
  company_name VARCHAR(32) NOT NULL COMMENT '保险公司名称',
  logo VARCHAR(100)  COMMENT '保险公司logo名称',
  PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE category(
  id INT(11) NOT NULL AUTO_INCREMENT,
  category_name VARCHAR(32) NOT NULL COMMENT '保险分类',
  description TEXT COMMENT '分类描述',
  parent_id INT(11) ,
  PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE images(
  id INT(11) NOT NULL AUTO_INCREMENT,
  img_name VARCHAR(255) NOT NULL COMMENT '图片名称',
  refered_id INT(11) COMMENT '关联到的ID,如产品id,或者保险公司id',
  type SMALLINT(2) NOT NULL DEFAULT 1 COMMENT '图片分类,0是logo,1产品图片',
  PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE tags(
  id INT(11) NOT NULL AUTO_INCREMENT,
  tag_name VARCHAR(32) NOT NULL COMMENT '标签名称',
  PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE clause (
  id INT(11) NOT NULL AUTO_INCREMENT,
  -- dupl_id INT(11) NOT NULL  COMMENT '条款的唯一id,用于表示多个保额和多个保期',
  clause_name VARCHAR(32) NOT NULL COMMENT '条款名称',
  -- price_unit VARCHAR(2) COMMENT '价格单位',
  description TEXT COMMENT '条款描述',
  category_id INT(11) NOT NULL  COMMENT '条款分类',
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ;

CREATE TABLE insurance (
  id INT(11) NOT NULL AUTO_INCREMENT,
  pro_name VARCHAR(32) NOT NULL COMMENT '产品名称',
  min_age INT(5) DEFAULT '0' COMMENT '最小年龄',
  max_age INT(5) NOT NULL COMMENT '最大年龄',
  notice TEXT COMMENT '重要告知',
  description TEXT COMMENT '描述',
  example TEXT COMMENT '投保样例',
  tags VARCHAR(255) DEFAULT NULL COMMENT '标签',
  suitable VARCHAR(32) COMMENT '适合人群',
  company_id INT(11) NOT NULL COMMENT '保险公司',
  category_id INT(11) NOT NULL COMMENT '保险分类',
  example_file VARCHAR(100) COMMENT '样本文件',
  price decimal(10,0) COMMENT '保费',
  sales_volume INT(11) NOT NULL DEFAULT 0 COMMENT '销量',
  buy_count SMALLINT(3) NOT NULL DEFAULT 1 COMMENT '可购买份数',
  valid_flag SMALLINT(1) NOT NULL DEFAULT 1 COMMENT '是否有效,1有效',
  create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time DATETIME,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE insu_clause (
  id INT(11) NOT NULL AUTO_INCREMENT,
  insu_id INT(11) NOT NULL COMMENT '产品id',
  clause_id INT(11) NOT NULL COMMENT '条款id',
  limits INT(11)  COMMENT '保额',
  insu_days INT(11) COMMENT '保期(/天)',
  -- isrange SMALLINT(1) NOT NULL DEFAULT 0 COMMENT '保期是否为范围值，范围值的价格按照天算',
  price decimal(10, 0) COMMENT '价格',
  create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time datetime NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ;

CREATE TABLE user (
  id INT(11) NOT NULL AUTO_INCREMENT,
  username VARCHAR(32) NOT NULL,
  password VARCHAR(32) DEFAULT NULL,
  role SMALLINT(2) NOT NULL DEFAULT 0,
  status SMALLINT(1) NOT NULL DEFAULT 1 COMMENT '状态０表示禁用',
  create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ;
